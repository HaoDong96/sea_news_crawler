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


class test_crawler(CrawlSpider):
    name = '7_Myanmar_commerce'
    allowed_domains = ['commerce.gov.mm']
    key_name = ['ocean','aquatic','marine ', 'fishery' ,  'harbor','warship','warcraft', 'fishing','coastal'
        , 'cargo+ship', 'cargo+vessel', 'cargo+boat'
            ,'maritime+policies','south+china+sea', 'blue+economy' ]
    # key_name=['ocean','water']
    base_url='http://www.commerce.gov.mm/en/search/node/{key}%20language%3Aen'


    def start_requests(self):
        # 用for和字符串插入的方法构成关键字链接循环入口
        for key in self.key_name:
            url = self.base_url.format(key=key)
            yield scrapy.Request(url=url, callback=self.parse_pages, dont_filter=True)
            #print(url)

    def parse_pages(self, response):
        try:
            print("parse_pages："+response.url)
            # '解析跳转到每篇文件链接'
            #print(response.body)
            for news_url in response.xpath('//ol[@class="search-results node-results"]'
                                           '/li[@class="search-result"]/h3/a/@href').extract():
                print("news url:"+news_url)
                yield scrapy.Request(news_url,callback=self.parse_news, dont_filter=True)
        except Exception as error:
            log(error)

    def parse_news(self, response):
        try:
            print("parse:"+response.url)
            #print(response.body)
            item = NewsItem()
            item['url'] = response.url
            item['country_code'] = "7"#"".join(response.xpath('//*[@property="v:summary"]/text()').extract())
            item['country_name']="Myanmar"
            item['source']="http://www.commerce.gov.mm"
            # image="".join(response.xpath('//section[@id="block-views-newsroom-page-block-1"]').extract())
            # if image:
            #     item['image']=image
            # else:
            #     item['image']=None
            item['image_urls'] = None

            item['content']= str("".join(response.xpath('//div[@class="field-item even"]').extract()).replace("img ", " "))
            #print("content"+item['content'])

            item['title']="".join(response.xpath('//*[@id="page-title"]/text()').extract())
            item['time']=None#"".join(response.xpath('//*[@id="container_content"]/div[3]/p/em/text()').extract())
            item['crawled_time']=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            #print("title:" + item['title'])#print(item['title'])
            yield item
        except Exception as error:
            log(error)
