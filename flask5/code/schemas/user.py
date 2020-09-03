from marshmallow import Schema, fields, INCLUDE, EXCLUDE


class UserSchema(Schema):
    class Meta:
        load_only = ("password",)
        dump_only = ("id","activated")
    id = fields.Int()
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    activated = fields.Bool()
    email = fields.Str(required=True)

    
    