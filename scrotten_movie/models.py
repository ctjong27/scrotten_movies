import uuid
from django.db import models

class ScrottenMovie(models.Model):
    movie_id = models.CharField('Movie Id', primary_key=True, max_length=255, unique=True)
    name = models.CharField('Name', max_length=255, unique=True)
    genre = models.CharField('Genre', max_length=255, unique=True)
    year = models.CharField('Year', max_length=255, unique=True)
    gross_sales = models.CharField('Gross Sales', max_length=255, unique=True)
    
    def __str__(self):
        return self.title