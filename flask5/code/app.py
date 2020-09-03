from flask import Flask, request, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from security import authenticate, identity
from resources.user import UserRegister, User, UserLogin, TokenRefresh,UserConfirm
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from marshmallow import ValidationError
from blacklist import BLACKLIST
from ma import ma 

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
api = Api(app)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["JWT_BLACKLIST_ENABLED"] = True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]
app.secret_key = "san francisco"


@app.before_first_request
def create_tables():
    db.create_all()

@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400


jwt = JWTManager(app)


@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {"is_admin": True}
    return {"is_admin": False}


@jwt.expired_token_loader
def expired_token_callback():
    return (
        jsonify({"description": "The token has expired", "error": "token expired"}),
        401,
    )


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token["jti"]
    return jti in BLACKLIST


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({"description": "Singature vertification failed"}), 401


@jwt.unauthorized_loader
def unauthroized_token_callback():
    return jsonify({"description": "Singature vertification failed"}), 401


@jwt.needs_fresh_token_loader
def need_fresh_token_callback():
    return jsonify({"description": "Singature vertification failed"}), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({"description": "Singature vertification failed"}), 401


# jwt = JWT(app, authenticate, identity)


api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")
api.add_resource(User, "/users/<int:user_id>")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UserConfirm, "/userconfirm/<int:user_id>")



if __name__ == "__main__":
    from db import db
    ma.init_app(app)
    db.init_app(app)
    app.run(port=3000, debug=True)
