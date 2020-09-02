from flask_restful import Resource, reqparse
from models.item import ItemModel
from utils.error import NotFoundError,InternalError



class ItemList(Resource):

    def get(self):
        try:
            items = ItemModel.get_all()
            return {"items": [item.json() for item in items]}
        except:
            return InternalError("was not able to fetch items").json()


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("name", type=str, required=True, help="this field cannot be blank")
    parser.add_argument("price", type=float, required=True, help="this field cannot be blank")
    parser.add_argument("store_id", type=int, required=True, help="this field cannot be blank")

    def post(self,name):
        existingItem = ItemModel.find_by_name(name)

        if existingItem:
            return InternalError("item exists").json()

        data = Item.parser.parse_args()
        item = ItemModel(**data)
        try:
            item.save()
            return {"message": "saved"},201
        except:
            return InternalError("was not able to add an item").json()


    def get(self, name):
        existingItem = ItemModel.find_by_name(name)
        if existingItem:
            return {"item": existingItem.json()}
        else:
            return InternalError("{} does not exist".format(name)).json()

    def delete(self,name):
         existingItem = ItemModel.find_by_name(name)
         if not existingItem:
             return InternalError("{} does not exist".format(name)).json()
         try:
             existingItem.delete()
             return {"message": "deleted"}
         except:
            return InternalError("was not able to remove {}".format(name)).json()

    
    def update(self, name):
         existingItem = ItemModel.find_by_name(name)
         if not existingItem:
            return InternalError("item does not exist").json()

         data = Item.parser.parse_args()
         item = ItemModel(**data)
        
         try:
             item.save()
             return {"message": "updated"}
         except:
             return InternalError("was not able to update").json()
        




