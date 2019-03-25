from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from hashlib import sha256
import os
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt
    )

from models.user import UserModel
from blacklist import BLACKLIST
from secret import LAUNCHCODE



# parser
_user_parser=reqparse.RequestParser()
_user_parser.add_argument('username',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
_user_parser.add_argument('password',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            # add argument to limit the charictors to 30
                            #can use RE to determine the types of passwords
                            )
# print(os.environ)
salt = os.environ['LAUNCH_CODE']

# Salt and Hash function for entering PW into DB
def salt_n_hash(password):
    return sha256(str.encode(password+salt)).hexdigest()


# *******USER RESOURCE*****
class UserRegister(Resource):
    def post(self):
        data = _user_parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        user = UserModel(data['username'], salt_n_hash(data['password']))
        #Hash the password:
        user.save_to_db()

        return {"message": "User created successfully."}, 201

class User(Resource):
    # returns a user as json
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User Not found'}, 404
        return user.json()

    # Deletes user
    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User Not found'},404
        user.delete_from_db()
        return {'message': 'User deleted.'}, 200

    # Updates user password
    #TODO: This needs to be only the user that is signed in
    @jwt_required
    @classmethod
    def put(cls, user_id):
        data = _user_parser.parse_args()
        user = UserModel.find_by_id(user_id)
        print(user.username, user.password)
        if user:
            user.password = salt_n_hash(data['password'])
        else:
            {'message':"user not found"}
        user.save_to_db()
        return {'message':'Password updated'}


class Recover_PW(Resource):
        # Updates user password
        #clearly this will need to be beefed up before handleing money
        #future improvments will be a more roubust Password recover ability
    @classmethod
    def put(cls):
        data = _user_parser.parse_args()
        user = UserModel.find_by_username(data['username'])
        if user:
            user.password = salt_n_hash(data['password'])
        else:
            {'message':"user not found"}
        user.save_to_db()
        return {'message':'Password updated'}



class UserList(Resource):
    # returns all UserRegister Need to make it only for user ID and user name
    @jwt_required
    def get(self):
        return {'users': list(map(lambda user: user.json(), UserModel.query.all()))}


class UserLogin(Resource):
    @classmethod
    def post(cls):
        #get data from pasrser
        data = _user_parser.parse_args()
        #find user in DB
        user = UserModel.find_by_username(data['username'])
        #Check password and unsalt DB password
        if user and safe_str_cmp(user.password, salt_n_hash(data['password'])):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        return{'message': 'Invalid credentials'}, 401


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti'] #jti is "JWT ID", a UID for JWt
        BLACKLIST.add(jti)
        return{'message': 'Successfully logged out.'}, 200


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'acces_token': new_token}, 200
