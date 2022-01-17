from django.db import models


class ScrottenMember(models.Model):
    member_id = models.CharField('Member Id', primary_key=True, max_length=255, unique=True)
    name = models.CharField('Name', max_length=255, unique=False)
    gender = models.CharField('Gender', max_length=255, unique=False)
    start_movie_year = models.PositiveIntegerField('Start Movie Year', blank=True, null=True)
    end_movie_year = models.PositiveIntegerField('End Movie Year', blank=True, null=True)
    start_tv_year = models.PositiveIntegerField('Start Tv Year', blank=True, null=True)
    end_tv_year = models.PositiveIntegerField('End Tv Year', blank=True, null=True)
    total_active_movie_year = models.PositiveIntegerField('Total Active Movie Year', blank=True, null=True)
    total_active_tv_year = models.PositiveIntegerField('Total Active Tv Year', blank=True, null=True)
    total_movie_count = models.PositiveIntegerField('Total Movie Cont', blank=True, null=True)
    total_tv_count = models.PositiveIntegerField('Total Tv Count', blank=True, null=True)
    
    def __str__(self):
        return self.movie_id