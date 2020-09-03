from typing import Dict, List, Union
from db import db

ItemJSON = Dict[str, Union[int, str, float]]


class ItemModel(db.Model):

    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"))
    store = db.relationship("StoreModel")

    def __init__(self, name: str, price: float, store_id: int):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self) -> ItemJSON:
        return {
            "name": self.name,
            "price": self.price,
            "store_id": self.store_id,
            "id": self.id,
        }

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def update(self) -> None:
        db.session.add(self)
        db.session.commit()
        # connection = sqlite3.connect(DATABASE)
        # cursor = connection.cursor()

        # query = "UPDATE items SET price=? WHERE name=?"

        # cursor.execute(query, (self.price, self.name))
        # connection.commit()
        # connection.close()

    def insert(self) -> None:
        db.session.add(self)
        db.session.commit()
        # connection = sqlite3.connect(DATABASE)
        # cursor = connection.cursor()
        # query = "INSERT INTO items VALUES (?, ?)"
        # cursor.execute(query, (self.name, self.price))
        # connection.commit()
        # connection.close()

    @classmethod
    def find_all(cls) -> List["ItemModel"]:
        return cls.query.all()

    @classmethod
    def find_by_name(cls, name: str) -> "ItemModel":
        return cls.query.filter_by(name=name).first()
        # connection = None
        # item = None
        # try:
        #     connection = sqlite3.connect(DATABASE)
        #     cursor = connection.cursor()

        #     query = "SELECT * FROM items WHERE name=?"

        #     result = cursor.execute(query, (name,))
        #     row = result.fetchone()
        #     connection.close()
        #     if row:
        #         item = cls(*row)
        #         return item
        #     else:
        #         item = None
        #         return item
        # except:
        #     item = None
        #     return item
