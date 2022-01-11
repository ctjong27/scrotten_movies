# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem
from scrotten_movie.models import ScrottenMovie
from scrotten_member.models import ScrottenMember


class ScrottenMovieItem(DjangoItem):
    django_model = ScrottenMovie
    # image_urls = scrapy.Field()
    # images = scrapy.Field()

class ScrottenMemberItem(DjangoItem):
    django_model = ScrottenMember
    # image_urls = scrapy.Field()
    # images = scrapy.Field()
