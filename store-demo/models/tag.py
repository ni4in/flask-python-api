from db import db


class TagModel(db.Model):
    __tablename__ = "tags"
<<<<<<< HEAD

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    store_id = db.Column(db.String(80), db.ForeignKey(
        "stores.id"), nullable=False)
    store = db.relationship(
        "StoreModel", back_populates="tags")
    items = db.relationship("ItemModel", back_populates = "tags", secondary = "item_tags")
=======
    
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80),unique=True,nullable=False)
    store_id = db.Column(db.String(80),db.ForeignKey("stores.id"),nullable=False)
    store = db.relationship("StoreModel",back_populates="tags",lazy="dynamic")
    items = db.relationship("ItemModel",back_populates = "tags",secondary = "ItemsTags")
    
    
    
>>>>>>> bff89bb1c7c63b08b3eb52c5eaeb3309630f7311
