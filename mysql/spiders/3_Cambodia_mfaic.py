# coding:utf-8

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from mysql.items import NewsItem
from scrapy import log
import urllib
import scrapy
import  re
import string
import time
from selenium import webdriver

class test_crawler(CrawlSpider):
    name = '3_Cambodia_mfaic'
    allowed_domains = ['mfaic.gov.kh']
    key_name = ['ocean','aquatic','marine ', 'fishery' ,  'harbor','warship','warcraft', 'fishing','coastal'
        , 'cargo+ship', 'cargo+vessel', 'cargo+boat'
            ,'maritime+policies','south+china+sea', 'blue+economy' ]
    # key_name=['ocean']
    base_url='https://www.mfaic.gov.kh/?s={key}'


    def start_requests(self):
        # 用for和字符串插入的方法构成关键字链接循环入口
        for key in self.key_name:
            url = self.base_url.format(key=key)
            yield scrapy.Request(url=url, callback=self.parse_pages, dont_filter=True)

    def parse_pages(self, response):
        try:
            print("parse_pages："+response.url)
            #print(response.body)
            # '解析跳转到每篇文件链接'
            for news_url in response.xpath('//div[@class="list-press"]/h4[@class="title-press"]/a/@href').extract():
                #news_url="https://www.dfa.gov.ph"+news_url
                print("news url:" + news_url)
                yield scrapy.Request(str(news_url),callback=self.parse_news, dont_filter=True)
                # '解析跳转到搜索结果的下一页'
            next_page = "".join(response.xpath(
                    '//div[@class="nav-links"]/a[@class="next page-numbers"]/@href').extract())
            if next_page:
                 yield scrapy.Request(next_page, callback=self.parse_pages, dont_filter=True)
        except Exception as error:
            log(error)

    def parse_news(self, response):
        try:
            print("parse:"+response.url)
            #print(str(response.css('.main-content *').extract()))

            item = NewsItem()
            item['url'] = response.url
            item['country_code'] = "3"
            item['country_name']="Cambodia"
            item['source'] = "https://www.mfaic.gov.kh"
            #content="".join(response.xpath('/html/body').extract())
            #content = re.sub('div class="col-sm-12 hidden-print"[\w\W]+sidebar', '', content).strip()
            # image="".join(response.xpath('//div[@class="item-page"]/div[@itemprop="articleBody"]/p/img').extract())
            # if image:
            #     item['image']=image
            # else:
            item['image_urls']=None
            #print("image:"+item['image'])
            item['content']="".join(response.xpath('//div[@class="content-detail"]').extract())
            #print("content:"+item['content'])

            item['title']="".join(response.xpath('//div[@class="content-detail"]/h4[@class="title-press"]/text()').extract())
            #print("title:" + item['title'])
            item['time']="".join(response.xpath('//div[@class="content-detail"]/div[@class="date"]/ul/li/text()').extract())
            #print("time:" + item['time'])
            item['crawled_time']=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            # #print(item['title'])
            yield item
        except Exception as error:
            log(error)
