import scrapy
from ..items import BookscrapyItem


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        books = response.css('article.product_pod')

        items = BookscrapyItem()

        # for book in books:
        name = books.css('h3 a::attr(title)').extract()
        price = books.css('.product_price .price_color').css(
            '::text').extract()
        url = books.css('h3 a::attr(href)').extract()

        items['name'] = name
        items['price'] = price
        items['url'] = url

        yield items

        next_page = books.css('li.next a::attr(href)').get()

        if next_page is not None:
            if 'catalogue/' in next_page:
                next_page_url = 'https://books.toscrape.com/' + next_page
            else:
                next_page_url = 'https://books.toscrape.com/catalogue/' + next_page

            yield response.follow(next_page_url, callback=self.parse)
