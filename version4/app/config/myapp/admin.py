from django.contrib import admin
from .models import User

@admin.register(User)
class TelegramUser(admin.ModelAdmin):

    list_display = ('phone_number', 'adress', 'is_active')
