import os

from flask import Flask, render_template, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

# Modules turn on as they are created
from db import db
from blacklist import BLACKLIST
from resources.user import (UserRegister,
        User,
        UserList,
        UserLogin,
        TokenRefresh,
        UserLogout,
        Recover_PW
        )
from resources.item import Item, ItemList
from resources.store import Store, StoreList
#TEST#


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTATIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLCKLIST_TOKEN_CHACKS'] = ['access', 'refresh']
app.secret_key = 'alien'
api = Api(app)

# Create DB:
@app.before_first_request
def create_tables():
    db.create_all()

# Auth (turn on later)
jwt = JWTManager(app)

@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity ==1:
        return {'is_admin': True}
    return {'is_admin': False}

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST

@jwt.expired_token_loader
def epired_token_callback():
    return jsonify({
        'description': "Your security token has expired.",
        'error': 'token_expired'
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):  # we have to keep the argument here, since it's passed in by the caller internally
    return jsonify({
        'message': 'Signature verification failed.',
        'error': 'invalid_token'
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        "description": "Request does not contain an access token.",
        'error': 'authorization_required'
    }), 401

@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        "description": "The token is not fresh.",
        'error': 'fresh_token_required'
    }), 401

@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        "description": "The token has been revoked.",
        'error': 'token_revoked'
    }), 401


# ITEM
api.add_resource(ItemList, '/')
api.add_resource(Item, '/item/<string:name>')
# Store
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
# User
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserList, '/users')
api.add_resource(UserLogin, '/auth')
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(Recover_PW, '/recover')


db.init_app(app)
if __name__ == '__main__':
    app.run(port=5000, debug=True)
