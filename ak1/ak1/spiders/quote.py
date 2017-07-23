import scrapy
from urllib.parse import urljoin

class QuoteSpider(scrapy.Spider):
    name = "quote_spider"
    start_urls=['http://quotes.toscrape.com/page/1/']
    
    def parse(self,response):
        for quote in response.xpath('.//div[@class="quote"]'):
            url=urljoin(response.url,quote.xpath('.//span[2]/a/@href').extract_first())
            yield scrapy.Request(url,callback=self.parse_author,dont_filter=True,meta={'item':{
                'text':quote.xpath('.//span[@class="text"]/text()').extract_first().strip('\“').strip('\”'),
                'author':quote.xpath('.//span[2]/small[@class="author"]/text()').extract_first(),
                'tags':quote.xpath('.//div[@class="tags"]/a[@class="tag"]/text()').extract(),
            }})
            
        next_page=response.xpath('.//li[@class="next"]/a/@href').extract_first()
        if next_page is not None:
            yield response.follow(next_page,self.parse)
        
    def parse_author(self,response):
        item = response.meta['item']
        item['birthday'] = response.xpath('.//span[@class="author-born-date"]/text()').extract_first(),
        item['location'] = response.xpath('.//span[@class="author-born-location"]/text()').extract_first().strip(" in"),
        return item