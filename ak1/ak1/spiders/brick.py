import scrapy

class BrickSetSpider(scrapy.Spider):
    name = "brickset_spider"
    start_urls=['http://brickset.com/sets/year-2016']
    
    def parse(self,response):
        for brickset in response.css('.set'):
            yield{
                'name':brickset.css('.meta h1 a::text').extract_first(),
                'tags':brickset.css('.meta div.tags a::text').extract(),
                'image':brickset.css('img ::attr(src)').extract_first(),
                'pieces':brickset.xpath('.//div[@class="col"]/dl/dt[contains(.,"Pieces")]/following::dd[1]/a/text()').extract_first(),
                'minifigs':brickset.xpath('.//div[@class="col"]/dl/dt[contains(.,"Minifigs")]/following::dd[1]/a/text()').extract_first(),
                'price':brickset.xpath('.//div[@class="col"]/dl/dt[contains(.,"RRP")]/following::dd[1]/text()').extract_first(),
                'availability':brickset.xpath('.//div[@class="col"]/dl/dt[contains(.,"Availability")]/following::dd[1]/text()').extract_first(),
            }
        next_page=response.css('.pagination li.next a::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)