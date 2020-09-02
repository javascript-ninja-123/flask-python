from flask_jwt import JWT, jwt_required
from flask_restful import Resource, reqparse
import sqlite3


DATABASE = 'data.db'

class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("price", type=float, required=True, help="This field is required")
  
    
    @jwt_required()
    def get(self, name):
        item = Item.find_by_name(name)
        if item:
            return item,200
        else:
            return {"message": "item not found"}, 404
    
    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()
        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'], item['price']))
        connection.commit()
        connection.close()


    @classmethod
    def find_by_name(cls, name):
        connection = None
        item = None
        try:
            connection = sqlite3.connect(DATABASE)
            cursor = connection.cursor()

            query = "SELECT * FROM items WHERE name=?"

            result = cursor.execute(query, (name,))
            row = result.fetchone()
            connection.close()
            if row:
                item = {'name': row[0], 'price': row[1]}
                return item
            else:
                item = None
                return item
        except:
            item = None
            return item



    @jwt_required()
    def post(self, name):
        if Item.find_by_name(name):
            return {"mesage":"name already taken"}, 400
        data = Item.parser.parse_args()
        item = {"name": name, "price": data['price']}
    
        try:
            Item.insert(item)
            return item, 201
        except:
            return {"mesage": "was not able to save"}, 400

    @classmethod
    def update(cls, update_item):
            connection = sqlite3.connect(DATABASE)
            cursor = connection.cursor()

            query = "UPDATE items SET price=? WHERE name=?"

            cursor.execute(query, (update_item['price'], update_item['name']))
            connection.commit()
            connection.close()

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = Item.find_by_name(name)
        if item is None:
         updated_item = {'name': name, "price": data['price']}
         try:
             Item.insert(updated_item)
             return item, 201
         except:
             return {"message":"not working"}, 500
        else:
            try:
                Item.update(updated_item)
                return updated_item, 200
            except:
                return {"message": "not working"}, 500


    @jwt_required()
    def delete(self,name):
        if Item.find_by_name(name) is None:
            return {"mesage": "item does not exist"}
        
        try:
            connection = sqlite3.connect(DATABASE)
            cursor = connection.cursor()
            query = "DELETE FROM items WHERE name=?"
            cursor.execute(query, (name,))
            connection.commit()
            connection.close()
            return {"message": "deleted"}, 200
        except:
            return {"message": "was not able to remove"},400





class ItemList(Resource):
    @jwt_required()
    def get(self):
        try:
            connection = sqlite3.connect(DATABASE)
            cursor = connection.cursor()

            query = "SELECT * FROM items"
            items = []
            for row in cursor.execute(query):
                items.append({"name": row[0], "price": row[1]})
            connection.close()
            return items
        except:
            return {"message":"was not able to fetch"}, 500

