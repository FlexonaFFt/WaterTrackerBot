#type: ignore
from django.db import models
from django.db.models.functions.text import CharField

# Пользователь
class User(models.Model):
    phone_number = models.CharField(max_length=11)
    adress = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.phone_number
