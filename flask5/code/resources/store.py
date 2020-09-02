from flask_restful import Resource, reqparse
from models.store import StoreModel


class Store(Resource):
    parser  = reqparse.RequestParser()
    parser.add_argument("name", type=str, required=True, help="this field cannot be blank")



    def get(self,name):
        store = StoreModel.find_by_name(name)
        if store is None:
            return {"message": "does not exist"}, 400
        return store.json(), 200


    def post(self, name):
        if StoreModel.find_by_name(name):
            return {"message": "already exists"}, 400
        data = Store.parser.parse_args()
        store = StoreModel(**data)
        try:
            store.save_to_db()
            return {"message": "created"}, 201
        except:
            return {"message": "failed"}, 500


    
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store is None:
            return {"message": "does not exist"}, 400
        try:
            store.delete_from_db()
            return {"message":"deleted"}, 200
        except:
            return {"message":"cannot delete"}, 500
        


class StoreList(Resource):
    def get(self):
        return {"stores": [store.json() for store in StoreModel.query.all()]},200

    


