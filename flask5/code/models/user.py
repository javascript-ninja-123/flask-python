import sqlite3
from flask_restful import Resource, reqparse
from db import db
DATABASE = 'data.db'

class UserModel(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def json(self):
        return {
            'id':self.id,
            'username':self.username
        }

    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
        # user = None
        # connection = None
        # try:
        #     connection = sqlite3.connect(DATABASE)
        #     cursor = connection.cursor()
        #     query = "SELECT * FROM users WHERE id=?"
        #     result = cursor.execute(query, (_id,))
        #     row = result.fetchone()
        #     if row:
        #         user = cls(*row)
        #     else:
        #         user = None
        # except Exception:
        #     print("did not work")
        #     user = None
        # finally:
        #     if connection:
        #         connection.close()
        # return user

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
        # user = None        
        # connection = None
        # try:
        #     connection = sqlite3.connect(DATABASE)
        #     cursor = connection.cursor()
        #     query = "SELECT * FROM users WHERE username=?"
        #     result = cursor.execute(query, (username,))
        #     row = result.fetchone()
        #     if row:
        #         user = cls(*row)
        #     else:
        #         user = None
        # except Exception:
        #     print("did not work")
        #     user = None
        # finally:
        #     if connection:
        #         connection.close()
        # return user