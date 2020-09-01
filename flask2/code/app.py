from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity


app = Flask(__name__)
api = Api(app)
app.secret_key = "Los Angeles"
jwt = JWT(app, authenticate, identity)

items = []


class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("price", type=float, required=True, help="This field is required")

    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x:x['name'] == name, items), None)
        return item, 200 if item else 400
    
    @jwt_required()
    def post(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is not None:
            return {"message": "item name is taken"}, 400
        
        data = Item.parser.parse_args()

        item = {'name': name, 'price': data["price"]}
        items.append(item)
        return item, 201

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = next(filter(lambda x:x['name'] == name, items), None)
        if item is None:
            item = {"name": name, "price": data["price"]}
            items.append(item)
        else:
            item.update(data)
        return item, 200

    @jwt_required()
    def delete(self,name):
        global items
        items = list(filter(lambda x:x['name'] != name, items))
        return {"message": "item deleted"}, 200


class ItemList(Resource):
    @jwt_required()
    def get(self):
        return items



api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=3000, debug=True)



    


