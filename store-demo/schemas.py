from marshmallow import Schema, fields


class PlainItemSchema(Schema):
    id = fields.Int(dumps_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)


class PlainStoreSchema(Schema):
    id = fields.Int(dumps_only=True)
    name = fields.Str(required=True)


class PlainTagSchema(Schema):
    id = fields.Int(dumps_only=True)
    name = fields.Str()


class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()


class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
<<<<<<< HEAD
    tags = fields.List(fields.Nested(PlainTagSchema(), dump_only = True))
=======
    tags = fields.Nested(PlainTagSchema(), dump_only=True)
>>>>>>> bff89bb1c7c63b08b3eb52c5eaeb3309630f7311


class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)


class TagSchema(PlainTagSchema):
<<<<<<< HEAD
    # store id is passed via url so this may or may not be there
    store_id = fields.Int(load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    items = fields.List(fields.Nested(PlainItemSchema()),dump_only = True)

class TagAndItemSchema(Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)
=======
    store_id = fields.Int(
        load_only=True
    )  # store id is passed via url so this may or may not be there
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    items = fields.Nested(PlainItemSchema(), dump_only=True)


class TagItems(Schema):

    message = fields.Str()
    item = fields.Nested(ItemSchema)
    tags = fields.Nested(TagSchema)
>>>>>>> bff89bb1c7c63b08b3eb52c5eaeb3309630f7311
