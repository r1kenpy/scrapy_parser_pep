# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PepParseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class PepParseItem(scrapy.Item):
    number = scrapy.Field()
    name = scrapy.Field()
    status = scrapy.Field()
