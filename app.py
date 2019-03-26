import os

from flask import Flask, render_template
from flask_restful import Api
from flask_jwt_extended import JWTManager

# Modules turn on as they are created
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
from blacklist import BLACKLIST
from db import db


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



if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
