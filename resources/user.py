from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required

from models.user import UserModel


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
                            )


# *******USER RESOURCE*****
class UserRegister(Resource):
    def post(self):
        data = _user_parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        user = UserModel(data['username'], data['password'])
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
        #Check password
        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        return{'message': 'Invalid credentials'}, 401
