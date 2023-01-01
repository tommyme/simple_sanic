from tortoise import fields
from tortoise.models import Model

class Account(Model):
    username = fields.CharField(max_length=30, unique=True)
    password = fields.TextField()
    
    def __str__(self) -> str:
        return f"<account username: {self.username} id: {self.id}>"

