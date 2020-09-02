import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel
from utils.error import NotFoundError
from blacklist import BLACKLIST
from flask_jwt_extended import get_raw_jwt,jwt_required, create_access_token, create_refresh_token,jwt_refresh_token_required,get_jwt_identity
DATABASE = 'data.db'



class UserLogin(Resource):
    parser  = reqparse.RequestParser()
    parser.add_argument("username", type=str, required=True, help="this field cannot be blank")
    parser.add_argument('password', type=str, required=True, help="this field cannot be blank")


    @classmethod
    def post(cls):
        data = cls.parser.parse_args()

        user = UserModel.find_by_username(data['username'])
        # user does not exist
        if not user:
            return NotFoundError("user not found").to_json()
        
        if user.password == data["password"]:
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token':refresh_token
            }, 200
        
        return NotFoundError("password does not match").to_json()
        



class User(Resource):


    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return NotFoundError("user not found").to_json()
        return user.json()
        
            

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return NotFoundError("user not found").to_json()
        user.delete_from_db()
        
        return {"message":"deleted"}, 200


class UserRegister(Resource):


    parser  = reqparse.RequestParser()
    parser.add_argument("username", type=str, required=True, help="this field cannot be blank")
    parser.add_argument('password', type=str, required=True, help="this field cannot be blank")
        

    def post(self):
        data = UserRegister.parser.parse_args()
        # connection = None
        # try:
        if UserModel.find_by_username(data['username']):
            return {"message":"user already exists"}, 400
            
        user = UserModel(**data)
        user.save_to_db()
            # connection = sqlite3.connect(DATABASE)
            # cursor = connection.cursor()
            # query = "INSERT INTO users VALUES (NULL, ?, ?)"
            # cursor.execute(query, (data['username'], data['password']))
            # connection.commit()
            # connection.close()
        return {'message': "user created successfully"}, 201

        # except Exception:
        #     return {'message': "cannot sign up"}, 400


class TokenRefresh(Resource):

    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        if current_user:
            access_token = create_access_token(identity=current_user, fresh=False)
            return {"access_token": access_token}, 200

        else:
            return {"message": "nope"},400
        
        
class UserLogOut(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        BLACKLIST.add(jti)