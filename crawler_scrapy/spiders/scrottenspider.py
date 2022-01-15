import scrapy
from crawler_scrapy.items import ScrottenWebItem #, ScrottenMemberItem , ScrottenMovieItem
from scrapy.spiders import CrawlSpider


# class ScrottenSpider(CrawlSpider):

#     name = 'scrottenspider'
#     allowed_domains = ['rottentomatoes.com']

#     # Process Rotten Tomato Movies from 1950 until 2025
#     # start_urls = ['https://www.rottentomatoes.com/top/bestofrt/?year=' + str(i) for i in range(1950, 2025)]
#     start_urls = ['https://www.rottentomatoes.com/top/bestofrt/?year=' + str(i) for i in range(2020, 2021)]


    
#     # enter the link and in the new page, retrieve the information found within the callback
#     def parse(self, response):
#         rows = response.xpath('//*[@class="table"]/tr/td[3]/a/@href').extract()
#         link = 'https://www.rottentomatoes.com/m/nomadland'
#         yield response.follow(url=link, callback=self.parse_movie_item)
        
        
        
#         # rows = response.xpath('//*[@class="table"]/tr/td[3]/a/@href').extract()
#         # for row in rows:
#         #     link = 'https://www.rottentomatoes.com' + row
            
#         #     # enter movies by yielding (returning, with option to continued data processing)
#         #     yield scrapy.Request(url=link, callback=self.parse_movie_item)
            
            
            

#     def parse_movie_item(self, response):
#         print('FLAG 1111111111111111')
#         # enter cast members
#         rows = response.xpath('//*[@data-qa="cast-crew-item"]/div[1]/a/@href').extract()
#         print(rows)
#         rows = list(set(rows))
#         print(rows)
#         for row in rows:
#             link = 'https://www.rottentomatoes.com' + row
#             yield scrapy.Request(url=link, meta={'item':i}, callback=self.parse_member_item)
            
#         return 
    
#     def parse_member_item(self, response):
#         print('FLAG 22222222222222222222')
#         i = ScrottenWebItem()
#         i['member_id'] = response.url[30:]
#         i['name'] = "asd"
#         i['ethnicity'] = "asd"
#         i['start_movie_year'] = 1234
#         i['end_movie_year'] = 2345
#         i['start_tv_year'] = 3456
#         i['end_tv_year'] = 4567
#         i['total_active_movie_year'] = 5678
#         i['total_active_tv_year'] = 6789
#         i['total_movie_count'] = 3
#         i['total_tv_count'] = 5
#         return i
    
    
    
    
# import scrapy
# from crawler_scrapy.items import ScrottenMemberItem, ScrottenMovieItem
# from scrapy.spiders import CrawlSpider


class ScrottenSpider(CrawlSpider):

    name = 'scrottenspider'
    allowed_domains = ['rottentomatoes.com']

    # Process Rotten Tomato Movies from 1950 until 2025
    # start_urls = ['https://www.rottentomatoes.com/top/bestofrt/?year=' + str(i) for i in range(1950, 2025)]
    start_urls = ['https://www.rottentomatoes.com/top/bestofrt/?year=' + str(i) for i in range(2020, 2021)]

    # enter the link and in the new page, retrieve the information found within the callback
    def parse(self, response):
        rows = response.xpath('//*[@class="table"]/tr/td[3]/a/@href').extract()
        for row in rows:
            link = 'https://www.rottentomatoes.com' + row
            
            # enter movies
            yield scrapy.Request(url=link, callback=self.parse_movie_item)
            
    def parse_movie_item(self, response):
        i = ScrottenWebItem()
        i['movie_id'] = response.url[30:]
        i['name'] = response.css('h1.scoreboard__title ::text').extract_first()
        i['genre'] = response.css('div.meta-value.genre ::text').extract_first().replace(' ','').replace('\n','')
        i['year'] = response.css('p.scoreboard__info ::text').extract_first()[:4]
        i['gross_sales'] = response.selector.xpath('//*[@class="meta-row clearfix"]//div[text()[contains(.,"Box Office (Gross USA):")]]/parent::*//div[@class="meta-value"]/text()').extract_first()
        i['approval_percentage'] = response.css('score-board ::attr(tomatometerscore)').extract_first()
    
        # enter cast members
        rows = response.xpath('//*[@data-qa="cast-crew-item"]/div[1]/a/@href').extract()
        rows = list(set(rows))
        for row in rows:
            link = 'https://www.rottentomatoes.com' + row
            yield scrapy.Request(url=link, meta={'item':i}, callback=self.parse_movie_item)

    
    def parse_member_item(self, response):
        i = response.request.meta['item']
        i['member_id'] = response.url[30:]
        i['name'] = "asd"
        i['ethnicity'] = "asd"
        i['start_movie_year'] = 1234
        i['end_movie_year'] = 2345
        i['start_tv_year'] = 3456
        i['end_tv_year'] = 4567
        i['total_active_movie_year'] = 5678
        i['total_active_tv_year'] = 6789
        i['total_movie_count'] = 3
        i['total_tv_count'] = 5
        yield i 
    