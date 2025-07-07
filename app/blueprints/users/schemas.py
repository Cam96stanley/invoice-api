from app.models import User
from app.extensions import ma

class UserSchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = User
    load_instance = True

user_schema = UserSchema()
return_user_schema = UserSchema(exclude=("password",))
return_users_schema = UserSchema(many=True, exclude=("password",))