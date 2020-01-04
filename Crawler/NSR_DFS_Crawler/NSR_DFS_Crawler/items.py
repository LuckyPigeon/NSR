# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NsrDfsCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ClassItem(scrapy.Item):
	_id = scrapy.Field()
	URL = scrapy.Field()
	parent = scrapy.Field()
	collection = scrapy.Field()

class ObjectItem(scrapy.Item):
	_id = scrapy.Field()
	URL = scrapy.Field()
	collection = scrapy.Field()

class ContentItem(scrapy.Item):
	_id = scrapy.Field()
	Content = scrapy.Field()
	collection = scrapy.Field()