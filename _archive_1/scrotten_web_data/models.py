from django.db import models


class ScrottenWebData(models.Model):
    
    web_data_id = models.CharField('Web Data Id', primary_key=True, max_length=255, unique=True)
    
    movie_id = models.CharField('Movie Id', max_length=255, unique=True)
    movie_name = models.CharField('Name', max_length=255, unique=False)
    movie_genre = models.CharField('Genre', max_length=255, unique=False)
    movie_year = models.PositiveIntegerField('Year', blank=True, null=True)
    movie_gross_sales = models.PositiveIntegerField('Gross Sales', blank=True, null=True)
    movie_approval_percentage = models.PositiveIntegerField('Approval Percentage', blank=True, null=True)
    
    member_id = models.CharField('Member Id', max_length=255, unique=True)
    member_name = models.CharField('Name', max_length=255, unique=False)
    member_birth_year = models.PositiveIntegerField('Birth Year', blank=True, null=True)
    member_gender = models.CharField('Gender', max_length=255, unique=False)
    member_start_movie_year = models.PositiveIntegerField('Start Movie Year', blank=True, null=True)
    member_end_movie_year = models.PositiveIntegerField('End Movie Year', blank=True, null=True)
    member_start_tv_year = models.PositiveIntegerField('Start Tv Year', blank=True, null=True)
    member_end_tv_year = models.PositiveIntegerField('End Tv Year', blank=True, null=True)
    member_total_active_movie_year = models.PositiveIntegerField('Total Active Movie Year', blank=True, null=True)
    member_total_active_tv_year = models.PositiveIntegerField('Total Active Tv Year', blank=True, null=True)
    member_total_movie_count = models.PositiveIntegerField('Total Movie Cont', blank=True, null=True)
    member_total_tv_count = models.PositiveIntegerField('Total Tv Count', blank=True, null=True)
    
    def __str__(self):
        return self.movie_id