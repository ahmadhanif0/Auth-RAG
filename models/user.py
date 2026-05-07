from tortoise.models import Model
from tortoise import fields

class User(Model):
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=200)
    email = fields.CharField(max_length=200)
    password = fields.CharField(max_length=300)
    is_verified = fields.BooleanField(default=False)
    otp_code = fields.CharField(max_length=6, null=True)
    otp_expiry = fields.DatetimeField(null=True)