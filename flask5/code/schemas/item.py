from ma import ma
from models.item import ItemModel
from models.store import StoreModel

class ItemSchema(ma.ModelSchema):
    class Meta:
        model = ItemModel
        load_only = ("store",)
        include_fk = True
