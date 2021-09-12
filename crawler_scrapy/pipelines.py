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

        ScrottenMovie.objects.create(
            title=title,
        )

        return item
