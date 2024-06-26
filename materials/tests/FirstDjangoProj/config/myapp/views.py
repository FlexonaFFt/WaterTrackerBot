from django.shortcuts import render
from rest_framework import viewsets
from .models import Author, Book, Genre
from .serializers import BookSerializer, BookCreateSerializer

def authors(request):
    authors = Author.objects.all()
    context = {
        'authors': authors
    }
    return render(request, 'authors.html', context)

def books(request):
    books = Book.objects.all()
    context = {
        'books': books
    }
    return render(request, 'books.html', context)

def genres(request):
    genres = Genre.objects.all()
    context = {
        'genres': genres
    }
    return render(request, 'genres.html', context)

def add_book(request):
    return render(request, 'add_book.html')

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return BookCreateSerializer
        return BookSerializer
