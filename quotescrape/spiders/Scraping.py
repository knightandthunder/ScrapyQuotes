import scrapy
from ..items import QuotescrapeItem
class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        "https://quotes.toscrape.com",
    ]

    def parse(self, response):
        for quote in response.css("div.quote"):
            yield {
                "text": quote.css("span.text::text").get(),
                "author": quote.css("small.author::text").get(),
                "tags": quote.css("div.tags a.tag::text").getall(),
            }
        next_page = response.css("li.next a::attr(href)").get()
        # if next_page is not None:
        #     yield response.follow(next_page,callback = self.parse)
        yield from response.follow_all(css="ul.pager a",callback=self.parse)

class QuoteSpider(scrapy.Spider):
    name = "newquotes"
    start_urls = ['http://quotes.toscrape.com']

    def parse(self,response):

        items = QuotescrapeItem()
        all_div_quotes = response.css('div.quote')

        for quotes in all_div_quotes:

            title = quotes.css('span.text::text').extract()
            author = quotes.css('.author::text').extract()
            tag = quotes.css('.tag::text').extract()

            items['title']=title
            items['author']=author
            items['tags']=tag

            yield items

        next_page = response.css("li.next a::attr(href)").get()
        # if next_page is not None:
        #     yield response.follow(next_page,callback = self.parse)
        yield from response.follow_all(css="ul.pager a",callback=self.parse)
