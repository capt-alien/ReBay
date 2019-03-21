from flask import Flask
from flask_restful import Api
# from flask_jwt import jwt

# Liberarries from sub modules DELETE WHEN MODULES ARE FINISHED
# models
from db import db

# resources
from flask_restful import Resource, reqparse
# from flask_jwt import jwt_required

# Modules turn on as they are created
# from security import authenticate, identity
# from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTATIONS'] = True
app.secret_key = 'alien'
api = Api(app)

# Create DB:
@app.before_first_request
def create_tables():
    db.create_all()

# Auth (turn on later)
# jwt = JWT(app, authenticate, identity)

class UserModel(db.Model):
    __tablename__='users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

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

# *****Routes*******
# ITEM
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

# Store
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

# User
api.add_resource(UserRegister, '/register')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
