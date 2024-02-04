# Define here the models for your scraped items

# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

# process structures of storing the extracted data
# extracted data -> temporary containers (items) -> stored in database

import scrapy


class WebscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    quote = scrapy.Field()
    author = scrapy.Field()
    tag = scrapy.Field()
