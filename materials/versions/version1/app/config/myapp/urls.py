from django.urls import path
from .views import TestView

# Прописываем связи
urlpatterns = [
    path('test/', TestView.as_view(), name='test')
]
