from datetime import date

from django.db import models
from django.conf.global_settings import LANGUAGES


class Author(models.Model):
    name = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=256)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    pub_date = models.DateField(default=date.today)
    isbn = models.CharField(max_length=13, unique=True)
    pages = models.PositiveSmallIntegerField()
    cover_url = models.URLField()
    language = models.CharField(max_length=10, choices=LANGUAGES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} - {self.author}'
