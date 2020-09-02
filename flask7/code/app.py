from flask import Flask
from flask_restful import Api
from resources.user import UserSignUp, UserList,UserLogIn
from resources.item import Item, ItemList
from resources.store import Store,StoreList
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
api = Api(app)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.secret_key = "san francisco"


@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWTManager(app)

@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'description':"The token has expired",
        "error":"token expired"
    }), 401

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in BLACKLIST


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'description': "Singature vertification failed"
    }), 401

@jwt.unauthorized_loader
def unauthroized_token_callback():
    return jsonify({
        'description': "Singature vertification failed"
    }), 401

@jwt.needs_fresh_token_loader
def need_fresh_token_callback():
    return jsonify({
        'description': "Singature vertification failed"
    }), 401

@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'description': "Singature vertification failed"
    }), 401



api.add_resource(UserSignUp, '/register')
api.add_resource(UserList, '/users')
api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")
api.add_resource(UserLogIn, "/login")

if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(port=3000, debug=True)