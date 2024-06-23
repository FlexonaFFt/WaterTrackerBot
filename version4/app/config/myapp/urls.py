#type: ignore
from django.urls import path
from . import views

urlpatterns = [
    path('check_user/', views.check_user),
    path('register_user/', views.register_user),
]
