from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models import ItemModel, TagModel, StoreModel
from schemas import TagSchema,   TagAndItemSchema
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

blp = Blueprint("Tags", __name__, description="Operation on Tags")


@blp.route("/store/<string:store_id>/tag")
class TagsInStore(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store.tags.all()

    @blp.arguments(TagSchema)
    @blp.response(200, TagSchema)
    def post(self, tag_data, store_id):
        tag = TagModel(**tag_data, store_id=store_id)
        # checking for unique id
        if TagModel.query.filter(TagModel.store_id == store_id and TagModel.name == tag_data["name"]).first():
            abort(400, message="Tag with same {} already existis in the store {}".format(
                tag_data["name"], store_id))

        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        return tag


@blp.route("/item/<string:item_id>/<string:tag_id>")
class LinkTagsToItem(MethodView):
    @blp.response(201, TagSchema)
    def post(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)
        item.tags.append(tag)
        try:
            db.session.add(item)
            db.commit()
        except SQLAlchemyError:
            abort(500, message=" An error occured while inserting the tag")
        return tag

    @blp.response(200, TagAndItemSchema)
    def delete(seld, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)
        item.tags.remove(tag)
        try:
            db.session.add(item)
            db.commit()
        except SQLAlchemyError:
            abort(
                500, message="An error occured while inserting an item after removing tag")

        return {"message": "Item removed from tag", "item": item, "tag": tag}


@blp.route("/tag/<string:tag_id>")
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag

    @blp.response(202, description="deletes a tag if no item is tagged with it", example={"message": "Tag Deleted"})
    @blp.alt_response(400, description="Retured if the tag is assigned to one or more items. In this case, tag is not deleted")
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)

        if not tag.items:
            db.session.delete(tag)
            db.session.commmit()
            return {"message": "Tag Deleted"}
        abort(400, message="Could not delete tag. Make sure tag is not associated with any items, then try again")
