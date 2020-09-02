from flask_restful import Resource, reqparse
from models.user import UserModel
from utils.error import NotFoundError,InternalError
from flask_jwt_extended import get_raw_jwt,jwt_required, create_access_token, create_refresh_token,jwt_refresh_token_required,get_jwt_identity

class UserList(Resource):

    @classmethod
    def get(cls):
        try:
            users = UserModel.get_all()

            return {"users": [user.json() for user in users]}, 200

        except:
            return NotFoundError("users not found").json()



class UserLogIn(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username", type=str, required=True, help="this field cannot be blank")
    parser.add_argument("password", type=str, required=True, help="this field cannot be blank")

    @classmethod
    def post(cls):
        data = cls.parser.parse_args()
        existingUser = UserModel.find_by_username(data['username'])
        if not existingUser:
            return NotFoundError("{} not found".format(data["username"])).json()
        
        if existingUser.password == data["password"]:
            access_token = create_access_token(identity=existingUser.id, fresh=True)
            refresh_token = create_refresh_token(existingUser.id)
            return {
                "access_token": access_token,
                "refresh_token": refresh_token
            }

        
        else:
            return InternalError("password does not match").json()



class UserSignUp(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username", type=str, required=True, help="this field cannot be blank")
    parser.add_argument("password", type=str, required=True, help="this field cannot be blank")

    @classmethod
    def post(cls):
        data = cls.parser.parse_args()
        existingUser = UserModel.find_by_username(data['username'])
        if existingUser:
            return InternalError("user already exist").json()

        user = UserModel(**data)
        try:
            user.save()
            return {"message": "user saved"}, 200
        except:
            return InternalError("cannot save a user").json()

