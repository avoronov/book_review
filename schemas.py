from marshmallow import Schema, fields


class AuthorSchema(Schema):
    id = fields.Integer(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)


class PublisherSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.Str(required=True)


class BookSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.Str(required=True)
    brief = fields.Str(required=True)
    rate = fields.Integer(required=True)
    author_id = fields.Integer(load_only=True)
    publisher_id = fields.Integer(load_only=True)
    author = fields.Nested(AuthorSchema, dump_only=True)
    publisher = fields.Nested(PublisherSchema, dump_only=True)
