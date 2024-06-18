from django.contrib import admin
from .models import Author, Genre, Book

class BookInline(admin.TabularInline):
    model = Book

class AuthorAdmin(admin.ModelAdmin):
    inlines = [BookInline]

admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Book)
