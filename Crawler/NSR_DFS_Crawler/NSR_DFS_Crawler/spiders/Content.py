# -*- coding: utf-8 -*-
'''
@Description 小說爬蟲
@Author LuckyPigeon
'''
from NSR_DFS_Crawler.items import ClassItem, ObjectItem, ContentItem
from os.path import abspath, basename, dirname, splitext
from scrapy.http.request import Request
import os, scrapy

class CategorySpider(scrapy.Spider):
    name = "CategorySpider"

    allow_domains = [
        'http://www.bwsk.net/'
        ]

    start_urls = [
        'http://www.millionbook.net/index.html'
    ]

    def parse(self, response):
        item = ClassItem()

        item['_id'] = '龍騰世紀/首頁'
        item['URL'] = response.request.url
        item['parent'] = 'NULL'

        parentName = item['_id']

        # 解析出類別及其URL
        URL = response.xpath('//center/a/@href').extract()
        # 過濾上層或重複網址
        URL = [url for url in URL if basename(dirname(url)) != '..']
        URL = list(set(URL))
        CName = [response.xpath('//center/a[@href="{0}"]/text()'.format(url)).extract_first() for url in URL]

        for index in range(len(CName)):
            item['_id'] = CName[index]
            item['URL'] = URL[index]
            item['parent'] = parentName
            yield item

        for index in range(len(URL)):
            if URL[index] is not None or URL[index] is not '':
                yield scrapy.Request(url = response.urljoin(URL[index]), callback = self.parseAuthor, meta = {'parent': CName[index]})

    def parseAuthor(self, response):
        item = ClassItem()

        # 解析出作者及其URL
        URL = response.xpath('//td[@width="16%"]/a/@href').extract()
        # 過濾上層或重複網址
        URL = [url for url in URL if basename(dirname(url)) != '..']
        URL = list(set(URL))
        CName = [response.xpath('//td[@width="16%"]/a[@href="{0}"]/text()'.format(url)).extract_first() for url in URL]

        for index in range(len(CName)):
            item['CName'] = CName[index]
            item['URL'] = URL[index]
            item['parent'] = response.meta['parent']
            yield item

        for index in range(len(URL)):
            if URL[index] is not None or URL[index] is not '':
                yield Request(url = response.urljoin(URL[index]), callback = self.parseNovel, meta = {'parent': CName[index]})

    def parseNovel(self, response):
        item = ClassItem()

        # 解析出書名及URL
        URL = response.xpath('//a/@href').extract()
        URL = [url for url in URL if basename(dirname(url)) != '..']
        URL = list(set(URL))

        CName = [response.xpath('//a[@href="{0}"]/text()'.format(url)).extract_first() for url in URL]
        
        for index in range(len(CName)):
            item['_id'] = CName[index]
            item['URL'] = URL[index]
            item['parent'] = response.meta['parent']
            yield item


class AuthorSpider(scrapy.Spider):
    '''
        爬取作者名稱以及其書籍，目前以武俠為例
    '''
    name = "AuthorSpider"
    
    allow_domains = [
        'http://www.bwsk.net/wx/'
        ]

    start_urls = [
        'http://www.bwsk.net/wx/index.html'
    ]

    ''' 
    def __init__(self, *args, **kwargs):
        super(AuthorSpider, self).__init__(*args, **kwargs)

        start_urls = [
            self.allow_domains[0] + kwargs.get('key')
        ]
    '''

    def parse(self, response):
        item = ClassItem()

        item['_id'] = '武俠小說'
        item['URL'] = response.request.url
        item['parent'] = '龍騰世紀'
        item['collection'] = 'Class'

        parentName = item['_id']

        # 解析出作者及其URL
        URL = response.xpath('//td[@width="16%"]/a/@href').extract()
        # 過濾上層或重複網址
        URL = [url for url in URL if basename(dirname(url)) != '..']
        URL = list(set(URL))
        CName = [response.xpath('//td[@width="16%"]/a[@href="{0}"]/text()'.format(url)).extract_first() for url in URL]


        for index in range(len(CName)):
            item['_id'] = CName[index]
            item['URL'] = URL[index]
            item['parent'] = parentName
            item['collection'] = 'Class'
            yield item
    
        for index in range(len(URL)):
            if URL[index] is not None or URL[index] is not '':
                print(URL[index])
                yield Request(url = response.urljoin(URL[index]), callback = self.parseNovel, meta = {'parent': CName[index]})

    def parseNovel(self, response):
        item = ClassItem()

        # 解析出書名及URL
        URL = response.xpath('//a/@href').extract()
        URL = [url for url in URL if basename(dirname(url)) != '..']
        URL = list(set(URL))

        CName = [response.xpath('//a[@href="{0}"]/text()'.format(url)).extract_first() for url in URL]
        
        for index in range(len(CName)):
            item['_id'] = CName[index]
            item['URL'] = URL[index]
            item['parent'] = response.meta['parent']
            item['collection'] = 'Class'
            yield item
        
class ChapterSpider(scrapy.Spider):
    '''
        爬取小說的目錄，目前以武俠為例
    '''
    name = "ChapterSpider"
    
    allow_domains = [
        'http://www.bwsk.net/wx/'
    ]
    
    def __init__(self, *args, **kwargs):
        super(ChapterSpider, self).__init__(*args, **kwargs)

        self.start_urls = [
            self.allow_domains[0] + kwargs.get('path')
        ]

    def parse(self, response):
        item = ObjectItem()

        # 解析出章回名稱及URL
        URL = response.xpath('//a/@href').extract()
        URL = [url for url in URL if basename(dirname(url)) != '..']
        URL = list(set(URL))
        CName = [response.xpath('//a[@href="{0}"]/text()'.format(url)).extract_first() for url in URL]

        for index in range(len(CName)):
            item['_id'] = CName[index]
            item['URL'] = URL[index]
            item['collection'] = 'Object'
            yield item

        for index in range(len(URL)):
            if URL[index] is not None or URL[index] is not '':
                print(URL[index])
                yield Request(url = response.urljoin(URL[index]), callback = self.parseContent, meta = {'parent': CName[index]})
        
    def parseContent(self, response):
        item = ContentItem()

        # 解析出內容
        item['_id'] = response.meta['parent']
        item['Content'] = response.xpath('//td[@class="tt2"]/text()').extract()
        item['collection'] = 'Content'
        yield item

class ContentSpider(scrapy.Spider):
    name = "ContentSpider"

    allow_domains = [
        'http://www.bwsk.net/wx/'
    ]

    def __init__(self, *args, **kwargs):
        super(ContentSpider, self).__init__(*args, **kwargs)

        self.start_urls = [
            self.allow_domains[0] + kwargs.get('path')
        ]

    def parse(self, response):
        item = ContentItem()

        # 解析出內容
        item['Content'] = response.xpath('//td[@class="tt2"]/text()').extract()
        item['collection'] = 'Content'
        yield item