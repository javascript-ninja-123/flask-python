from typing import Dict, List, Union
from flask_restful import Resource, reqparse
from flask import request,url_for
from db import db
from libs.mailgun import Mailgun
from requests import Response


USER_JSON = Dict[str, Union[str, int]]




class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    activated = db.Column(db.Boolean, default=False)

    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.activated = False
        self.email = email
        
        
    def send_confirmation_email(self) -> Response:
        
        link = request.url_root[0:-1] + url_for("userconfirm", user_id=self.id)
        return Mailgun.send_confirmation_email([self.email], "confirmation", f"click the link {link}")

      
        

    def json(self) -> USER_JSON:
        return {"id": self.id, "username": self.username}

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
        
    
    @classmethod
    def find_by_email(cls, email: str) -> "UserModel":
        return cls.query.filter_by(email=email).first()
        

    @classmethod
    def find_all(cls) -> List["UserModel"]:
        return cls.query.all()

    @classmethod
    def find_by_id(cls, _id) -> "UserModel":
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
    def find_by_username(cls, username) -> "UserModel":
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
