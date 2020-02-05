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

class WikiInfoItem(scrapy.Item):
    '''
      書籍相關基本資訊
    '''

    title = scrapy.Field()
    author = scrapy.Field()
    location = scrapy.Field()
    lang = scrapy.Field()
    category = scrapy.Field()
    type = scrapy.Field()
    publisher = scrapy.Field()
    pubDate = scrapy.Field()
    puDateZh = scrapy.Field()
    format = scrapy.Field()
    pages = scrapy.Field()
    lastBook = scrapy.Field()
    nextBook = scrapy.Field()
    abstract = scrapy.Field()
    background = scrapy.Field()
    version = scrapy.Field()
    evaluate = scrapy.Field()
    collection = scrapy.Field()

class WikiWorksItem(scrapy.Item):
    '''
      書籍改編作品以及周邊產品
    '''

    episode = scrapy.Field()
    movie = scrapy.Field()
    game = scrapy.Field()
    mobileGame = scrapy.Field()
    collection = scrapy.Field()

class WikiCharacterItem(scrapy.Item):
    '''
      書籍角色列表專用資料結構
    '''

    parent = scrapy.Field()
    child = scrapy.Field()
    collection = scrapy.Field()

class InfoItem(scrapy.Item):
    '''
      博客來產品頁面中書籍基本資訊
    '''

    author = scrapy.Field()
    publisher = scrapy.Field()
    date = scrapy.Field()
    lang = scrapy.Field()
    price = scrapy.Field()
    sale = scrapy.Field()
    salePrice = scrapy.Field()
    saleLimit = scrapy.Field()

class BookItem(scrapy.Item):
    '''
      博客來產品頁面中相關書籍資訊，如，“買了此商品的人，也買了”
    '''

    title = scrapy.Field()
    img = scrapy.Field()
    url = scrapy.Field()
    sale = scrapy.Field()
    salePrice = scrapy.Field()

class AbstractItem(scrapy.Item):
    '''
      博客來產品頁面中書籍基本資訊
    '''

    content = scrapy.Field()

class DetailItem(scrapy.Item):
    '''
      博客來產品頁面中書籍基本資訊
    '''

    ISBN = scrapy.Field()
    specification = scrapy.Field()
    location = scrapy.Field()
    classification = scrapy.Field()
