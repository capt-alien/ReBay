from flask import Flask
from flask_restful import Api
from flask_jwt import jwt

# Liberarries from sub modules DELETE WHEN MODULES ARE FINISHED
# models
from db import db

# resources
from flask_restful import Resource, reqparse
# from flask_jwt import jwt_required

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

# Create DB:
@app.before_first_request
def create_tables():
    db.create_all()


# Auth (turn on later)
# jwt = JWT(app, authenticate, identity)


# item model
class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(percision=2))

    # Forign Key for store
    # store_id = db.Column(db.Integer, db.ForeignKey('Stores.id'))
    # store = db.relationship('StoreModel')

    def __init__(self, name, price): #Add_later , store_id):
        self.name = name
        self.price = price
        # sel.store_id = store_id

    def json(self):
        return{'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


# item resources
class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This Field Cannot Be left blank!"
                        )
    # parser.add_argument('store_id',
    #                     type=int,
    #                     required=True,
    #                     help="Every item needs a store_id."
    #                     )

    # @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404


    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'messae':'Item deleted.'}
        return {'message':'Item not found.'}, 404

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item:
            item.price = data['price']

        else:
            item = ItemModel(name, **data)

        item.save_to_db()

        return item.json()

class ItemList(Resource):
    def get(self):
        return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}


# ITEM
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

# Store
# api.add_resource(Store, '/store/<string:name>')
# api.add_resource(StoreList, '/stores')

# User
# api.add_resource(UserRegister, '/register')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
