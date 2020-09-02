from flask_jwt_extended import (
    jwt_required, 
    get_jwt_claims,
    jwt_optional,
    get_jwt_identity,
    fresh_jwt_required
)
from flask_restful import Resource, reqparse
from models.item import ItemModel
import sqlite3


DATABASE = 'data.db'

class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("price", type=float, required=True, help="This field is required")
    parser.add_argument("store_id", type=int, required=True, help="This field is required")
  
    
    @jwt_required
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(),200
        else:
            return {"message": "item not found"}, 404




    @jwt_required
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"mesage":"name already taken"}, 400
        data = Item.parser.parse_args()
        item = ItemModel(name, data["price"], data["store_id"])
    
        try:
            item.insert()
            return item.json(), 201
        except:
            return {"mesage": "was not able to save"}, 400



    @jwt_required
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
             item = ItemModel(name, data["price"], data["store_id"])
        else:
            item.price = data["price"]

        item.update()
        return {"message": "updated"}, 200

        #  try:
        #      updated_item.insert()
        #      return {"message":"created it"}, 201
        #  except:
        #      return {"message":"not working"}, 500
        # else:
        #     try:
        #         updated_item.update()
        #         return {"message": "updated"}, 200
        #     except:
        #         return {"message": "not working"}, 500


    @fresh_jwt_required
    def delete(self,name):
        claims = get_jwt_claims()
        if not cliams["is_admin"]:
            return {"message": "admin privilegae not given"}, 400
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"message": "deleted"}, 200
        else:
            return {"mesage": "item does not exist"},400

        # if ItemModel.find_by_name(name) is None:
        #     return {"mesage": "item does not exist"}
        
        # try:
        #     connection = sqlite3.connect(DATABASE)
        #     cursor = connection.cursor()
        #     query = "DELETE FROM items WHERE name=?"
        #     cursor.execute(query, (name,))
        #     connection.commit()
        #     connection.close()
        #     return {"message": "deleted"}, 200
        # except:
        #     return {"message": "was not able to remove"},400





class ItemList(Resource):
    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()
        items = [item.json() for item in ItemModel.query.all()]
        # list(map(lambda x: x.json(), ItemModel.query().all()))
        if user_id:
            return {"items": items}, 200
        else:
            return {"items": [item['name'] for item in items], "message": "you should login"},200
        # try:
        #     connection = sqlite3.connect(DATABASE)
        #     cursor = connection.cursor()

        #     query = "SELECT * FROM items"
        #     items = []
        #     for row in cursor.execute(query):
        #         items.append({"name": row[0], "price": row[1]})
        #     connection.close()
        #     return items
        # except:
        #     return {"message":"was not able to fetch"}, 500