from django.db import models

class Movie(models.Model):
    title = models.CharField('Title',max_length=255, unique=True)
    
    def __str__(self):
        return self.title