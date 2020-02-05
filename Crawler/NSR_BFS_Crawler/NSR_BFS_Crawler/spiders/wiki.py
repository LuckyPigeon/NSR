# -*- coding: utf-8 -*-
from NSR_BFS_Crawler.items import WikiInfoItem, WikiWorksItem, WikiCharacterItem
from os.path import abspath, basename, dirname, splitext
from scrapy.http.request import Request
from w3lib.html import remove_tags
import os, scrapy


class WikiSpider(scrapy.Spider):
    name = 'WikiSpider'
    allowed_domains = ['zh.wikipedia.org']
    start_urls = [
        'https://zh.wikipedia.org/wiki/%E5%A4%A9%E9%BE%99%E5%85%AB%E9%83%A8_(%E5%B0%8F%E8%AF%B4)', 
        'https://zh.wikipedia.org/wiki/%E5%A4%A9%E9%BE%99%E5%85%AB%E9%83%A8%E8%A7%92%E8%89%B2%E5%88%97%E8%A1%A8'
    ]

    def parse(self, response):
        # yield scrapy.Request(url = self.start_urls[0], callback = self.parseBasicInfo)
        # yield scrapy.Request(url = self.start_urls[0], callback = self.parseWorks)
        yield scrapy.Request(url = self.start_urls[1], callback = self.parseCharacter)

    def textExtract(self, response, start, key):
        ''' 利用前後目錄名稱擷取當前目錄下的文字 '''

        result = []
        startId = response.xpath('//h2/span[@id="' + response.xpath('//h2/span[@class="mw-headline"]/@id')[start].extract() + '"]/preceding-sibling::span/@id').extract()[0]
        endId = response.xpath('//h2/span[@id="' + response.xpath('//h2/span[@class="mw-headline"]/@id')[start+1].extract() + '"]/preceding-sibling::span/@id').extract()[0]
        
        for i in response.xpath('//h2/span[@id="' + startId + '"]/../following-sibling::' + key).extract():
            for j in response.xpath('//h2/span[@id="' + endId + '"]/../preceding-sibling::' + key).extract():
                if i == j:
                    result.append(remove_tags(i).strip())
        
        return result
    
    def dlExtract(self, response, items):
        ''' 
          解析 dl tag 下的物件，函式參數為 1. response = <dl selector> 2. items = result array
          例如：
            父：三司
            子：范驊 (司馬)、巴天石 (司空)、華赫艮 (司徒)
          則在 WIKI 上顯示為
            * 三司 (<ul><li>三司</li></ul>)
              * 范驊 (司馬)、巴天石 (司空)、華赫艮 (司徒) (<dl><dd><ul><li>范驊 (司馬)、巴天石 (司空)、華赫艮 (司徒)</dl></dd></ul></li>)
        '''

        item = WikiCharacterItem()
        item['collection'] = "Character"
        item['parent'] = remove_tags(response.xpath('./preceding-sibling::ul/li')[-1].extract()).strip() # 解析出 dl tag 的父物件

        ''' dl 下的 xpath 有可能為 "./dd/ul/li"，也有可能只有 "./dd" 而已，而兩種不同的 xpath 需要不同解析的方式 '''
        if response.xpath('./dd/ul/li') != []:
            ''' 如果是 "./dd/ul/li" 路徑，則需依序拜訪底下每個子物件 '''
            for value in response.xpath('./dd/ul/li'):
                item['child'] = remove_tags(value.extract()).strip() # 解析 li 下的子物件字串
                items.append(item) # 集滿父與子物件之後就放進 items 陣列
                ''' 如 li 的下一個 sibling 為 dl，則代表還有下一層子物件，因此需要遞迴呼叫 dlExtract 函式 '''
                try:
                    if value.xpath('../following-sibling::*').xpath('name()')[0].extract() == 'dl':
                        items = self.dlExtract(value.xpath('../following-sibling::dl')[0], items) # 更新 items 後回傳
                except IndexError:
                    print('已經沒有小孩囉！！！')
        else:
            item['child'] = remove_tags(response.extract()).strip()
            items.append(item)

        return items

    def parseBasicInfo(self, response):
        ''' 解析基本資訊方框 '''

        item = WikiInfoItem()
        item['collection'] = "Information"

        item['title'] = response.xpath('//table[@class="infobox vcard"]/caption/b/text()').extract()[0] # 書籍名稱
        item['author'] = response.xpath('//table[@class="infobox vcard"]/tbody/tr')[1].xpath('./td/a/text()').extract()[0] # 作者
        item['location'] = response.xpath('//table[@class="infobox vcard"]/tbody/tr')[2].xpath('./td/a/text()').extract()[0] # 出版地點
        item['lang'] = response.xpath('//table[@class="infobox vcard"]/tbody/tr')[3].xpath('./td/text()').extract()[0] # 語言
        item['category'] = response.xpath('//table[@class="infobox vcard"]/tbody/tr')[4].xpath('./td/text()').extract()[0] # 題材
        item['type'] = response.xpath('//table[@class="infobox vcard"]/tbody/tr')[5].xpath('./td/text()').extract()[0] # 類型
        item['publisher'] = response.xpath('//table[@class="infobox vcard"]/tbody/tr')[6].xpath('./td/a/text()').extract()[0] # 出版商
        item['pubDate'] = response.xpath('//table[@class="infobox vcard"]/tbody/tr')[7].xpath('./td/text()').extract()[0] # 出版日期
        item['puDateZh'] = response.xpath('//table[@class="infobox vcard"]/tbody/tr')[8].xpath('./td/text()').extract()[0] # 中文出版日期
        item['format'] = response.xpath('//table[@class="infobox vcard"]/tbody/tr')[9].xpath('./td/text()').extract()[0] # 媒介
        item['pages'] = response.xpath('//table[@class="infobox vcard"]/tbody/tr')[10].xpath('./td/text()').extract()[0] # 頁數
        item['lastBook'] = response.xpath('//table[@class="infobox vcard"]/tbody/tr')[11].xpath('./td/a/text()').extract()[0] # 上一部作品
        item['nextBook'] = response.xpath('//table[@class="infobox vcard"]/tbody/tr')[12].xpath('./td/a/text()').extract()[0] # 下一部作品
        toremove = response.xpath('//div[@id="toc"]/preceding-sibling::p').extract()
        item['abstract'] = [remove_tags(x).strip() for x in toremove] # 摘要
        item['background'] = self.textExtract(response, 0, 'p')
        item['version'] = self.textExtract(response, 4, 'ul/li')
        item['evaluate'] = self.textExtract(response, 5, 'p')

        yield item

    def parseWorks(self, response):
        ''' 將書籍改編作品以及周邊產品爬取下來 '''
        
        item = WikiWorksItem()
        item['collection'] = "Works"

        toremove = response.xpath('//h3/span[@class="mw-headline"]')[-1].xpath('../following-sibling::ul')[0].xpath('./li').extract()
        item['movie'] = [remove_tags(x) for x in toremove] # 電影
        
        toremove = response.xpath('//h2/span[@class="mw-headline"]')[-4].xpath('../following-sibling::ul')[0].xpath('./li').extract()
        item['game'] = [remove_tags(x) for x in toremove] # 電腦遊戲

        toremove = response.xpath('//h2/span[@class="mw-headline"]')[-3].xpath('../following-sibling::ul')[0].xpath('./li').extract()
        item['mobileGame'] = [remove_tags(x) for x in toremove] # 手機遊戲

        yield item

    def parseCharacter(self, response):
        ''' 爬取書籍角色以及介紹 '''

        item = WikiCharacterItem()
        item['collection'] = "Character"
        characters = response.xpath('//div[@id="toc"]/following-sibling::*') # 角色的原始碼列
        h2cursor = ''
        h3cursor = ''

        for ch in characters:
            if ch.xpath('name()').extract()[0] == 'h2':
                h2cursor = remove_tags(ch.xpath('./span[@class="mw-headline"]').extract()[0])
            elif ch.xpath('name()').extract()[0] == 'h3':
                h3cursor = remove_tags(ch.xpath('./span[@class="mw-headline"]').extract()[0])
                item['parent'] = h2cursor
                item['child'] = h3cursor
                yield item
            elif ch.xpath('name()').extract()[0] == 'ul':
                chArr = ch.xpath('./li').extract()
                item['parent'] = h3cursor
                if len(chArr) == 1:
                    item['child'] = remove_tags(chArr[0])
                    yield item
                else:
                    for value in chArr:
                        item['child'] = remove_tags(value)
                        yield item
            elif ch.xpath('name()').extract()[0] == 'dl':
                items = self.dlExtract(ch, [])
                print('items:')
                print(items)
                if len(items) == 1:
                    yield items[0]
                else:
                    for value in items:
                        print('value:')
                        print(value)
                        yield value
            else:
                item['parent'] = h3cursor
                item['child'] = remove_tags(ch.extract())
                yield item
