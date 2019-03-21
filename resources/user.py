from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.user import UserModel


# *******USER RESOURCE*****
class UserRegister(Resource):
    parser=reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )


    def post(self):
        data = UserRegister.parser.parse_args()

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
    @jwt_required()
    def get(self):
        return {'users': list(map(lambda user: user.json(), UserModel.query.all()))}
