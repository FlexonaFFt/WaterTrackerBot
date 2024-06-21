from django.urls import path, include
from .views import authors, books, genres
from rest_framework.routers import DefaultRouter
from .views import BookViewSet
from .views import add_book

router = DefaultRouter()
router.register(r'books', BookViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('authors/', authors, name='authors'),
    path('books/', books, name='books'),
    path('genres/', genres, name='genres'),
    path('add-book/', add_book, name='add_book')
]
