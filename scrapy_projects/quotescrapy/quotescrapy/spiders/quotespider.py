# CREATING AND RUNNING THE FIRST SPIDER CRAWLER

# importing the library
import scrapy
from ..items import WebscrapyItem

# creating class


class QuoteSpider(scrapy.Spider):
    # creating variable to store the name of the webscrapper
    name = 'quotes'
    # creating variable to store page number
    page_number = 2
    # creating variable to store the url link of page 1
    start_urls = ['https://quotes.toscrape.com/page/1/']

    # defining a function name parse

    def parse(self, response):

        # creating an instance variable for WebscrapyItem class
        items = WebscrapyItem()

        # creating a new variable to extract the quotes using css selectors
        # we are not using .extract() function
        all_div_quotes = response.css('div.quote')
        # we are just locating the div tag and inside it has span tag along with text as class

        for quotes in all_div_quotes:

            # creating a new variable for extracting quotes
            quote = quotes.css('span.text::text').extract()
            # creating a new variable for extracting authors
            author = quotes.css('.author::text').extract()
            # creating a new variable for extracting tags
            tag = quotes.css('.tag::text').extract()

            # using the blueprint of the class WebscrapyItem()
            # storing the data in the proper designated containers
            items['quote'] = quote
            items['author'] = author
            items['tag'] = tag

            # returning the output using yield keyword
            yield items

        # creating a new variable to go to the next page
        next_page = 'https://quotes.toscrape.com/page/' + \
            str(QuoteSpider.page_number) + '/'

        # if the next page is not less than 11
        if QuoteSpider.page_number < 11:

            # then add number 1 to the current page number
            QuoteSpider.page_number += 1

            # using yield keyword and follow keyword
            # go to the next page and starts the parse function to scrape data
            # and this will continue till the last page
            yield response.follow(next_page, callback=self.parse)
