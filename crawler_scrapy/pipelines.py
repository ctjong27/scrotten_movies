# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrotten_movie.models import ScrottenMovie

def clean_title(param):
    return param

class ScrottenCrawlerPipeline(object):

    def process_item(self, item, spider):
        title = clean_title(item['title'])

    # movie_id = models.CharField(max_length=255, unique=True)
    # name = models.CharField(max_length=255)
    # genre = models.CharField(max_length=255)
    # year = models.IntegerField(max_length=4)
    # gross_sales = models.BigIntegerField()

        ScrottenMovie.objects.create(
            title=title,
        )

        return item
