from django.urls import path
from .views import authors, books, genres

urlpatterns = [
    path('authors/', authors, name='authors'),
    path('books/', books, name='books'),
    path('genres/', genres, name='genres')
]
