import scrapy
from ..items import QuotestoscrapeItem

class QuotesToScrape(scrapy.Spider):
    name = 'QuotesToScrape'
    page_no = 2
    start_urls = [
        'http://quotes.toscrape.com/page/1/'
    ]
    count = 0

    def parse(self,response):
        item = QuotestoscrapeItem()
        all_div_quotes = response.css("div.quote")
        for q in all_div_quotes:
            quotes = q.css("span.text::text").extract()
            by = q.css("small.author::text").extract()
            tags = q.css('.tag::text').extract()

            item['quotes'] = quotes
            item['by'] = by
            item['tags'] =tags

            yield{
                'quotes':quotes,
                'by':by,
                'tags':tags,
                'count':self.count
            }
        next_page = 'http://quotes.toscrape.com/page/'+str(self.page_no)+'/'
        if(self.page_no < 11):
            self.page_no+=1
            yield response.follow(next_page,callback= self.parse)









