# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrotten_movie.models import ScrottenMovie
from decimal import Decimal

def clean_movie_id(param):
    return param

def clean_name(param):
    return param

def clean_genre(param):
    if param is None:
        return ''

    return param

def clean_year(param):
    return param

def clean_gross_sales(param):
    if param is None:
        return 0

    param = param.strip().replace('$', '')
    
    base = 0
    if 'K' in param:
        base = 1000
    if 'M' in param:
        base = 1000000
    if 'B' in param:
        base = 1000000000

    param = param.strip().replace('K', '')
    param = param.strip().replace('M', '')
    param = param.strip().replace('B', '')

    return Decimal(param) * base

def clean_approval_percentage(param):
    if param is None:
        return 0

    return param

class ScrottenCrawlerPipeline(object):

    def process_item(self, item, spider):
        movie_id = clean_movie_id(item['movie_id'])
        name = clean_name(item['name'])
        genre = clean_genre(item['genre'])
        year = clean_year(item['year'])
        gross_sales = clean_gross_sales(item['gross_sales'])
        approval_percentage = clean_approval_percentage(item['approval_percentage'])

        ScrottenMovie.objects.create(
            movie_id=movie_id,
            name=name,
            genre=genre,
            year=year,
            gross_sales=gross_sales,
            approval_percentage=approval_percentage,
        )

        return item
