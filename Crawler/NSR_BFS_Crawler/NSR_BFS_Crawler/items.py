# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NsrBfsCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class WikiItem(scrapy.Item):
    key = scrapy.Field()
    value = scrapy.Field()

class InfoItem(scrapy.Item):
    author = scrapy.Field()
    publisher = scrapy.Field()
    date = scrapy.Field()
    lang = scrapy.Field()
    price = scrapy.Field()
    sale = scrapy.Field()
    salePrice = scrapy.Field()
    saleLimit = scrapy.Field()

class BookItem(scrapy.Item):
    title = scrapy.Field()
    img = scrapy.Field()
    url = scrapy.Field()
    sale = scrapy.Field()
    salePrice = scrapy.Field()

class AbstractItem(scrapy.Item):
    content = scrapy.Field()

class DetailItem(scrapy.Item):
    ISBN = scrapy.Field()
    specification = scrapy.Field()
    location = scrapy.Field()
    classification = scrapy.Field()

class CharacterItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
