# # coding:utf-8
#
# from scrapy.spiders import CrawlSpider, Rule
# from scrapy.linkextractors import LinkExtractor
# from mysql.items import NewsItem
# from scrapy import log
# import urllib
# import scrapy
# import  re
# import string
# import time
#
#
# class test_crawler(CrawlSpider):
#     name = '6_Malaysia_miti'
#     allowed_domains = ['miti.gov.my']
#     key_name = ['ocean','aquatic','marine ', 'fishery','warship', 'fishing','coastal' 'blue+economy' ]
#     # key_name=['ocean']
#     base_url='http://www.miti.gov.my/index.php/search/results?search={key}'
#
#
#     def start_requests(self):
#         # 用for和字符串插入的方法构成关键字链接循环入口
#         for key in self.key_name:
#             url = self.base_url.format(key=key)
#             yield scrapy.Request(url=url, callback=self.parse_pages, dont_filter=True)
#             #print(url)
#
#     def parse_pages(self, response):
#         try:
#             print("parse_pages："+response.url)
#             # '解析跳转到每篇文件链接'
#             #print(response.body)
#             for news_url in response.xpath('//div[@id="search_result"]'
#                                            '/div[@class="search_result_item"]/a/@href').extract():
#                 print("news url:"+news_url)
#                 yield scrapy.Request(news_url,callback=self.parse_news, dont_filter=True)
#         except Exception as error:
#             log(error)
#
#     def parse_news(self, response):
#         try:
#             print("parse:"+response.url)
#             #print(response.body)
#             item = NewsItem()
#             item['url'] = response.url
#             item['country_code'] = "6"#"".join(response.xpath('//*[@property="v:summary"]/text()').extract())
#             item['country_name']="Malaysia"
#             # image="".join(response.xpath('//section[@id="block-views-newsroom-page-block-1"]').extract())
#             # if image:
#             #     item['image']=image
#             # else:
#             #     item['image']=None
#             item['image_urls'] = None
#             item['content']="".join(response.xpath('//*[@id="container_content"]/div[@class="editable"]').extract()).replace('src="','src="http://www.miti.gov.my/')
#             #print("content"+item['content'])
#             item['source']="http://www.miti.gov.my"
#             item['title']="".join(response.xpath('//*[@id="365"]/div[2]/div[1]/h1/text()').extract())
#             item['time']="".join(response.xpath('//*[@id="container_content"]/div[3]/p/em/text()').extract())
#             item['crawled_time']=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
#             # #print(item['title'])
#             yield item
#         except Exception as error:
#             log(error)





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
    name = '6_Malaysia_miti'
    allowed_domains = ['miti.gov.my']
    key_name = ['ocean','aquatic','marine ', 'fishery','warship', 'fishing','coastal' 'blue+economy' ]
    # key_name=['ocean']
    base_url='http://www.miti.gov.my/miti/resources/Media%20Release/Media_Release_-_Malaysia_Promotion_Programme_(MPP)_takes_centre_stage_in_Manila.pdf'


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
            for news_url in response.xpath('//div[@id="search_result"]'
                                           '/div[@class="search_result_item"]/a/@href').extract():
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
            item['country_code'] = "6"#"".join(response.xpath('//*[@property="v:summary"]/text()').extract())
            item['country_name']="Malaysia"
            # image="".join(response.xpath('//section[@id="block-views-newsroom-page-block-1"]').extract())
            # if image:
            #     item['image']=image
            # else:
            #     item['image']=None
            item['image_urls'] = None
            item['content']="".join(response.xpath('//*[@id="container_content"]/div[@class="editable"]').extract()).replace('src="','src="http://www.miti.gov.my/')
            #print("content"+item['content'])
            item['source']="http://www.miti.gov.my"
            item['title']="".join(response.xpath('//*[@id="365"]/div[2]/div[1]/h1/text()').extract())
            item['time']="".join(response.xpath('//*[@id="container_content"]/div[3]/p/em/text()').extract())
            item['crawled_time']=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            # #print(item['title'])
            yield item
        except Exception as error:
            log(error)
