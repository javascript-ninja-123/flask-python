import sqlite3
from flask_restful import Resource, reqparse

DATABASE = 'data.db'

class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password


    @classmethod
    def find_by_id(cls, _id):
        user = None
        connection = None
        try:
            connection = sqlite3.connect(DATABASE)
            cursor = connection.cursor()
            query = "SELECT * FROM users WHERE id=?"
            result = cursor.execute(query, (_id,))
            row = result.fetchone()
            if row:
                user = cls(*row)
            else:
                user = None
        except Error as e:
            print(e)
            user = None
        finally:
            if connection:
                connection.close()
        return user

    @classmethod
    def find_by_username(cls, username):
        user = None        
        connection = None
        try:
            connection = sqlite3.connect(DATABASE)
            cursor = connection.cursor()
            query = "SELECT * FROM users WHERE username=?"
            result = cursor.execute(query, (username,))
            row = result.fetchone()
            if row:
                user = cls(*row)
            else:
                user = None
        except Error as e:
            print(e)
            user = None
        finally:
            if connection:
                connection.close()
        return user


class UserRegister(Resource):


    parser  = reqparse.RequestParser()
    parser.add_argument("username", type=str, required=True, help="this field cannot be blank")
    parser.add_argument('password', type=str, required=True, help="this field cannot be blank")
        

    def post(self):
        data = UserRegister.parser.parse_args()
        connection = None
        try:
            if User.find_by_username(data['username']):
                return {"message":"user already exists"}, 400
            connection = sqlite3.connect(DATABASE)
            cursor = connection.cursor()
            query = "INSERT INTO users VALUES (NULL, ?, ?)"
            cursor.execute(query, (data['username'], data['password']))
            connection.commit()
            connection.close()
            return {'message': "user created successfully"}, 201

        except:
            return {'message': "cannot sign up"}, 400







