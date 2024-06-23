#type: ignore
from enum import unique
from django.db import models
from django.db.models.functions.text import CharField

# Пользователь
class User(models.Model):
    chat_id = models.CharField(max_length=15, unique=True)
    phone_number = models.CharField(max_length=11)
    adress = models.CharField(max_length=255)

    def __str__(self):
        return self.phone_number
