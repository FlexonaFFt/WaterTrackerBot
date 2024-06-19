from rest_framework import serializers
from .models import Author, Genre, Book

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name', 'biography']

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name', 'description']

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    genres = GenreSerializer(many=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'description', 'publication_date', 'num_pages', 'price', 'genres', 'author', 'is_bestseller']

class BookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'description', 'publication_date', 'num_pages', 'price', 'genres', 'author', 'is_bestseller']
