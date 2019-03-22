from flask import Flask, render_template
from flask_restful import Api
from flask_jwt_extended import JWTManager

# Modules turn on as they are created
from resources.user import UserRegister, User, UserList, UserLogin
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
jwt = JWTManager(app)

@jwt.user_claims_loader
def add_claims_to_jwt(identity):



# Home Route
@app.route('/')
def home():
    return render_template('index.html')

# ITEM
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
# Store
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
# User
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserList, '/users')
api.add_resource(UserLogin, '/auth')



if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
