# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# import mysql.connector

import os
from itemadapter import ItemAdapter
from pymongo import MongoClient
from dotenv import load_dotenv


class BookscrapyPipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        # strip all whitespaces from strings
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != 'description':
                value = adapter.get(field_name)
                adapter[field_name] = value[0].strip()

        # category and product_type to lowercase
        lowercase_keys = ['category', 'product_type']
        for lowercase_key in lowercase_keys:
            value = adapter.get(lowercase_key)
            adapter[lowercase_key] = value.lower()

        # price -> convert to float
        price_keys = ['price', 'price_excl_tax', 'price_incl_tax', 'tax']
        for price_key in price_keys:
            value = adapter.get(price_key)
            value = value.replace('£', '')
            adapter[price_key] = float(value)

        # availability -> extract number of books in stock
        availability_keys = adapter.get('availability')
        split_string_array = availability_keys.split('(')
        if len(split_string_array) < 2:
            adapter['availability'] = 0
        else:
            availability_array = split_string_array[1].split(' ')
            adapter['availability'] = int(availability_array[0])

        # reviews -> convert string to number
        review_string = adapter.get('reviews')
        adapter['reviews'] = int(review_string)

        # ratings -> convert text to number
        star_rating = adapter.get('ratings')
        split_star_array = star_rating.split(' ')
        star_text_value = split_star_array[1].lower()
        if star_text_value == "zero":
            adapter['ratings'] = 0
        elif star_text_value == "one":
            adapter['ratings'] = 1
        elif star_text_value == "two":
            adapter['ratings'] = 2
        elif star_text_value == "three":
            adapter['ratings'] = 3
        elif star_text_value == "four":
            adapter['ratings'] = 4
        elif star_text_value == "five":
            adapter['ratings'] = 5
        return item


# class SaveToMySQLPipeline:

#     def __init__(self):
#         self.create_connection()
#         self.create_table()

#     def create_connection(self):
#         self.conn = mysql.connector.connect(
#             host='localhost',
#             user='root',
#             passwd='12345@nil',
#             database='books'
#         )
#         self.curr = self.conn.cursor()

#     def create_table(self):
#         self.curr.execute("""DROP TABLE IF EXISTS books""")
#         self.curr.execute("""
#         CREATE TABLE IF NOT EXISTS books(
#             id int NOT NULL auto_increment,
#             url VARCHAR(255),
#             title text,
#             upc VARCHAR(255),
#             product_type VARCHAR(255),
#             price_excl_tax DECIMAL,
#             price_incl_tax DECIMAL,
#             tax DECIMAL,
#             price DECIMAL,
#             availability INTEGER,
#             reviews INTEGER,
#             ratings INTEGER,
#             category VARCHAR(255),
#             description text,
#             PRIMARY KEY (id)
#         )
#         """)

#     def process_item(self, item, spider):

#         self.curr.execute(""" insert into books (
#             url,
#             title,
#             upc,
#             product_type,
#             price_excl_tax,
#             price_incl_tax,
#             tax,
#             price,
#             availability,
#             reviews,
#             ratings,
#             category,
#             description
#             ) values (
#                 %s,
#                 %s,
#                 %s,
#                 %s,
#                 %s,
#                 %s,
#                 %s,
#                 %s,
#                 %s,
#                 %s,
#                 %s,
#                 %s,
#                 %s
#                 )""", (
#             item["url"],
#             item["title"],
#             item["upc"],
#             item["product_type"],
#             item["price_excl_tax"],
#             item["price_incl_tax"],
#             item["tax"],
#             item["price"],
#             item["availability"],
#             item["reviews"],
#             item["ratings"],
#             item["category"],
#             str(item["description"])
#         ))
#         self.conn.commit()

#         return item

#     def close_spider(self, spider):

#         # Close cursor & connection to database
#         self.curr.close()
#         self.conn.close()


# class SaveToMongoDBPipeline:

#     def __init__(self):
#         pass

#     def open_spider(self, spider):
#         self.db = get_mongodb_client()

#     def process_item(self, item, spider):
#         items_to_insert = []
#         if item:
#             items_to_insert.append(dict(item))

#         if len(items_to_insert) >= 10:
#             collection = self.db['books_db']
#             try:
#                 collection.insert_many(items_to_insert)
#                 self.logger.info("Inserted %d items", len(items_to_insert))
#             except pymongo.errors.PyMongoError as e:
#                 self.logger.error("Error inserting data: %s", e)
#             items_to_insert = []

#         return item


# Load environment variables (assuming .env file is in the same directory)
load_dotenv()


class SaveToMongoDBPipeline:

    def __init__(self):
        """Initializes the MongoDB connection using environment variables."""
        self.mongo_url = os.getenv("MONGODB_URL")
        self.mongo_db = os.getenv("MONGODB_DATABASE")

        self.client = MongoClient(self.mongo_url)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        items_to_insert = []
        if item:
            items_to_insert.append(dict(item))
        # if len(items_to_insert) >= 10:
            collection = self.db['books_db']
            collection.insert_many(items_to_insert)
            items_to_insert = []
        return item

    def close_spider(self, spider):
        """Closes the MongoDB connection."""
        self.client.close()
