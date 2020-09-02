from flask_restful import Resource, reqparse
from models.store import StoreModel
from utils.error import NotFoundError,InternalError
from flask_jwt_extended import (
    jwt_required, 
    get_jwt_claims,
    jwt_optional,
    get_jwt_identity,
    fresh_jwt_required
)


class StoreList(Resource):

    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()
        stores = StoreModel.get_all()
        store_array = [store.json() for store in stores]
        if user_id:
            return {"stores": store_array}
        else:
            return {"stores": [{'id': store['id']} for store in store_array]}


class Store(Resource):
      parser  = reqparse.RequestParser()
      parser.add_argument("name", type=str, required=True, help="this field cannot be blank")

      @jwt_required 
      def get(self, name):
          existingStore = StoreModel.find_by_name(name)
          if not existingStore:
              return NotFoundError("store not found").json()
          
          return {"store": existingStore.json()},200

      @jwt_required  
      def post(self, name):
          existingStore = StoreModel.find_by_name(name)
          if existingStore:
              return InternalError("store already exists").json()
          data = Store.parser.parse_args()
          store = StoreModel(**data)
          try:
              store.save()
              return {"message": "created"}
          except:
              return InternalError("was not able to save").json()

      

      



