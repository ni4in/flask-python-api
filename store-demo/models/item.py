from db import db


class ItemModel(db.Model):
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique = True, nullable = False)
    price = db.Column(db.Float(precision=2), unique = False, nullable= False)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), unique = False, nullable = False)
    store = db.relationship("StoreModel",back_populates="items")
<<<<<<< HEAD
    tags = db.relationship("TagModel", back_populates = "items", secondary = "item_tags")
=======
    tags = db.relationship("TagModel", back_populates="items",secondary="ItemTags")
>>>>>>> bff89bb1c7c63b08b3eb52c5eaeb3309630f7311
