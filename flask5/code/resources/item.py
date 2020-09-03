from flask_jwt_extended import jwt_required, fresh_jwt_required
from flask_restful import Resource, reqparse
from models.item import ItemModel

BLANK_ERROR = "This field {} is required"
ITEM_NOT_FOUND = "item not found"


class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        "price", type=float, required=True, help=BLANK_ERROR.format("price")
    )
    parser.add_argument(
        "store_id", type=int, required=True, help=BLANK_ERROR.format("store_id")
    )

    def get(self, name: str):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200
        else:
            return {"message": ITEM_NOT_FOUND}, 404

    @jwt_required
    def post(self, name: str):
        if ItemModel.find_by_name(name):
            return {"mesage": "name already taken"}, 400
        data = Item.parser.parse_args()
        item = ItemModel(name, data["price"], data["store_id"])

        try:
            item.insert()
            return item.json(), 201
        except:
            return {"mesage": "was not able to save"}, 400

    @jwt_required
    def put(self, name: str):
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
    def delete(self, name: str):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"message": "deleted"}, 200
        else:
            return {"mesage": "item does not exist"}, 400

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
    def get(self):

        items = [item.json() for item in ItemModel.query.all()]
        # list(map(lambda x: x.json(), ItemModel.query().all()))
        return {"items": items}, 200
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
