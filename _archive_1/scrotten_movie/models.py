from django.db import models


class ScrottenMovie(models.Model):
    movie_id = models.CharField('Movie Id', primary_key=True, max_length=255, unique=True)
    name = models.CharField('Name', max_length=255, unique=False)
    genre = models.CharField('Genre', max_length=255, unique=False)
    year = models.PositiveIntegerField('Year', blank=True, null=True)
    gross_sales = models.PositiveIntegerField('Gross Sales', blank=True, null=True)
    approval_percentage = models.PositiveIntegerField('Approval Percentage', blank=True, null=True)
    
    def __str__(self):
        return self.movie_id