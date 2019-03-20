from flask import flask
from flask_restful import Api
from flask_jwt import jwt

# Liberarries from sub modules DELETE WHEN MODULES ARE FINISHED





# Modules turn on as they are created
# from security import authenticate, identity
# from resources.user import UserRegister
# from resources.item import Item, ItemList
# from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTATIONS'] = True
app.secret_key = 'alien'
api = Api(app)

# Auth (turn on later)
jwt = JWT(app, authenticate, identity)

api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')



if __name__ = '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
