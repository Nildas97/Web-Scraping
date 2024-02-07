# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


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
