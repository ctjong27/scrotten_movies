from django.db import models


class ScrottenMovieToMember(models.Model):
    
    id = models.CharField('Id', primary_key=True, max_length=255, unique=True)
    
    movie_id = models.CharField('Movie Id', max_length=255, unique=True)
    member_id = models.CharField('Member Id', max_length=255, unique=True)
    
    def __str__(self):
        return self.id