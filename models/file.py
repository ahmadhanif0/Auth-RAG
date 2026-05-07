from tortoise.models import Model
from tortoise import fields

class File(Model):
    filename = fields.TextField()
    file_path = fields.TextField()
    file_type = fields.TextField()
    extracted_text = fields.TextField(null=True)
    is_active = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)