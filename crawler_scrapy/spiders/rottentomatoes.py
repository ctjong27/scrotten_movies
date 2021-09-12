
import scrapy
from crawler_scrapy.items import ScrottenMovieItem
from scrapy.spiders import CrawlSpider


class RottenTomatoesSpider(CrawlSpider):

    name = 'rottentomatoes'
    allowed_domains = ['rottentomatoes.com']
    start_urls = ['https://www.rottentomatoes.com/top/bestofrt/?year=2018',]

    def parse(self, response):
        rows = response.xpath('//*[@class="table"]/tr/td[3]/a/@href').extract()
        for row in rows:
            link = 'https://www.rottentomatoes.com' + row
            yield scrapy.Request(url=link, callback=self.parse_item)

    def parse_item(self, response):
        i = ScrottenMovieItem()
        i['title'] = response.css('h1.scoreboard__title ::text').extract_first()
        return i