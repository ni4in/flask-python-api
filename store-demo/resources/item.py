
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

blp = Blueprint("items", __name__, description="Operations on Items")


@blp.route("/item/<string:item_id>")
class Items(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)  # order of the decorator matters
    def put(self, item_data, item_id,):
        item = ItemModel.query.get(item_id)
        if item:
            item.name = item_data["name"]
            item.price = item["price"]
        else:
            item = ItemModel(id = item_id, **item_data)
        db.session.add(item)
        db.session.commit()
        return item

    # dont decorated as the responses are just messages  and similar for other delete methods too
    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item Deleted"}


@blp.route("/item")
class ItemList(MethodView):
    # using the instance for many outputs
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        # marshmallow will make the output to json so no need to jsonify
        return ItemModel.query.all()

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)
        try:
            db.session.add(item)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A store with that name already exists")
        except SQLAlchemyError:
            abort(500, message="An error occured while inserting the item in database")
        return item
