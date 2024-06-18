from django.shortcuts import render
from .models import Author, Book, Genre

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
