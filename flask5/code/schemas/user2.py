from ma import ma
from models.user import UserModel

class UseSchema2(ma.ModelSchema):
    class Meta:
        model = UserModel
        load_only = ("password", )