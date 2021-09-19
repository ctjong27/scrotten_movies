import scrapy
from crawler_scrapy.items import ScrottenMovieItem
from scrapy.spiders import CrawlSpider


class ScrottenSpider(CrawlSpider):

    name = 'scrottenspider'
    allowed_domains = ['rottentomatoes.com']

    # Process Rotten Tomato Movies from 1950 until 2025
    start_urls = ['https://www.rottentomatoes.com/top/bestofrt/?year=' + str(i) for i in range(1950, 2025)]

    def parse(self, response):
        rows = response.xpath('//*[@class="table"]/tr/td[3]/a/@href').extract()
        for row in rows:
            link = 'https://www.rottentomatoes.com' + row
            yield scrapy.Request(url=link, callback=self.parse_item)

    def parse_item(self, response):
        i = ScrottenMovieItem()
        i['movie_id'] = response.url[30:]
        i['name'] = response.css('h1.scoreboard__title ::text').extract_first()
        i['genre'] = response.css('div.meta-value.genre ::text').extract_first().replace(' ','').replace('\n','')
        i['year'] = response.css('p.scoreboard__info ::text').extract_first()[:4]
        i['gross_sales'] = response.selector.xpath('//*[@class="meta-row clearfix"]//div[text()[contains(.,"Box Office (Gross USA):")]]/parent::*//div[@class="meta-value"]/text()').extract_first()
        i['approval_percentage'] = response.css('score-board ::attr(tomatometerscore)').extract_first()
        return i