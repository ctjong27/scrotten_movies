import scrapy
from crawler_scrapy.items import ScrottenWebDataItem #, ScrottenMemberItem , ScrottenMovieItem
from scrapy.spiders import CrawlSpider
import random

class ScrottenSpider(CrawlSpider):

    name = 'scrottenspider'
    allowed_domains = ['rottentomatoes.com']

    # Process Rotten Tomato Movies from 1950 until 2025
    # start_urls = ['https://www.rottentomatoes.com/top/bestofrt/?year=' + str(i) for i in range(1950, 2025)]
    start_urls = ['https://www.rottentomatoes.com/top/bestofrt/?year=' + str(i) for i in range(2020, 2021)]

    # enter the link and in the new page, retrieve the information found within the callback
    def parse(self, response):
        rows = response.xpath('//*[@class="table"]/tr/td[3]/a/@href').extract()
        # link = 'https://www.rottentomatoes.com' + rows[0]
        for row in rows:
            print(row)
            link = 'https://www.rottentomatoes.com' + row
            
            # enter movies
            yield scrapy.Request(url=link, callback=self.parse_movie_item)
        # for x in range(0, 5):
        #     link = 'https://www.rottentomatoes.com' + rows[x]
            
        #     # enter movies
        #     yield scrapy.Request(url=link, callback=self.parse_movie_item)
            
    def parse_movie_item(self, response):
        i = ScrottenWebDataItem()
        
        # i['web_data_id'] = random.randint(1, 1000000)
        
        i['movie_id'] = response.url[30:]
        i['movie_name'] = response.css('h1.scoreboard__title ::text').extract_first()
        i['movie_genre'] = response.css('div.meta-value.genre ::text').extract_first().replace(' ','').replace('\n','')
        i['movie_year'] = response.css('p.scoreboard__info ::text').extract_first()[:4]
        i['movie_gross_sales'] = response.selector.xpath('//*[@class="meta-row clearfix"]//div[text()[contains(.,"Box Office (Gross USA):")]]/parent::*//div[@class="meta-value"]/text()').extract_first()
        i['movie_approval_percentage'] = response.css('score-board ::attr(tomatometerscore)').extract_first()
        
        yield i
        # # enter cast members
        # rows = response.xpath('//*[@data-qa="cast-crew-item"]/div[1]/a/@href').extract()
        # rows = list(set(rows))
        # for row in rows:
        #     link = 'https://www.rottentomatoes.com' + row
        #     yield scrapy.Request(url=link, meta={'item':i}, callback=self.parse_member_item)

    
    def parse_member_item(self, response):
        i = response.request.meta['item']
        i['member_id'] = response.url[30:]
        i['member_name'] = "asd"
        i['member_gender'] = "asd"
        i['member_start_movie_year'] = 2001
        i['member_end_movie_year'] = 2003
        i['member_start_tv_year'] = 2001
        i['member_end_tv_year'] = 2007
        i['member_total_active_movie_year'] = 5
        i['member_total_active_tv_year'] = 4
        i['member_total_movie_count'] = 3
        i['member_total_tv_count'] = 5
        
        print(i)
        yield i 
    