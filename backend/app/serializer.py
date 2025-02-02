from marshmallow import Schema, fields


class ArticleSchema(Schema):
    id = fields.Int()
    url = fields.Str()
    headline = fields.Str()
    thumbnail_url = fields.Str()
    website_id = fields.Int()
    created_at = fields.DateTime()


class WebsiteSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    url = fields.Str()
    favicon_url = fields.Str()
    articles = fields.List(fields.Nested(ArticleSchema))
    created_at = fields.DateTime()