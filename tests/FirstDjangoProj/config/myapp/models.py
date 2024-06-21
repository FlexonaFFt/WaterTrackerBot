from django.db import models

class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    biography = models.TextField(blank=True)

class Genre(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

class Book(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    publication_date = models.DateField()
    num_pages = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    genres = models.ManyToManyField(Genre)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    is_bestseller = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    def __str__(self):
        return self.title
