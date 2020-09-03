from flask import request
from flask_restful import Resource, reqparse
from models.user import UserModel
from utils.error import NotFoundError
from blacklist import BLACKLIST
from schemas.user import UserSchema
from marshmallow import ValidationError
from flask_jwt_extended import (
    get_raw_jwt,
    jwt_required,
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
)

user_schema = UserSchema()


class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "username", type=str, required=True, help="this field cannot be blank"
    )
    parser.add_argument(
        "password", type=str, required=True, help="this field cannot be blank"
    )

    @classmethod
    def post(cls):
        try:
            data = user_schema.load(request.get_json())


            user = UserModel.find_by_username(data["username"])
            # user does not exist
            if not user:
                return NotFoundError("user not found").to_json()

            if user.password == data["password"]:
                if not user.activated:
                    return {"message":"user not activated"}, 400
                access_token = create_access_token(identity=user.id, fresh=True)
                refresh_token = create_refresh_token(user.id)
                return {"access_token": access_token, "refresh_token": refresh_token}, 200

            return NotFoundError("password does not match").to_json()
        except ValidationError as err:
            return err.messages, 400


class User(Resource):
    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return NotFoundError("user not found").to_json()
        return user_schema.dump(user), 200

    @classmethod
    def delete(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return NotFoundError("user not found").to_json()
        user.delete_from_db()

        return {"message": "deleted"}, 200


class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        "username", type=str, required=True, help="this field cannot be blank"
    )
    parser.add_argument(
        "password", type=str, required=True, help="this field cannot be blank"
    )
    
    @classmethod
    def post(cls):
        try:
            data = user_schema.load(request.get_json())
            if UserModel.find_by_username(data["username"]):
                return {"message": "user already exists"}, 400
            if UserModel.find_by_email(data["email"]):
                return {"message": "email taken"},400
            user = UserModel(**data)
            user.save_to_db()
            user.send_confirmation_email()
            return {"message":"sent"}
        except ValidationError as err:
            return err.messages, 400
        # connection = None
        # try:
  
        # connection = sqlite3.connect(DATABASE)
        # cursor = connection.cursor()
        # query = "INSERT INTO users VALUES (NULL, ?, ?)"
        # cursor.execute(query, (data['username'], data['password']))
        # connection.commit()
        # connection.close()
       

        # except Exception:
        #     return {'message': "cannot sign up"}, 400


class TokenRefresh(Resource):
    @classmethod
    @jwt_refresh_token_required
    def post(cls):
        current_user = get_jwt_identity()
        if current_user:
            access_token = create_access_token(identity=current_user, fresh=False)
            return {"access_token": access_token}, 200

        else:
            return {"message": "nope"}, 400


class UserLogOut(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()["jti"]
        BLACKLIST.add(jti)
        

class UserConfirm(Resource):
    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "user not found"}, 404
        user.activated = True
        try:
            user.save_to_db()
            return {"message":"activated"}, 200
        except:
            return {"message": "was not able to save"}, 404
        
        
    
