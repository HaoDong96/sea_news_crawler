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
    name = '1_soa_gov'
    allowed_domains = ['soa.gov.cn']
    start_urls={'http://www.soa.gov.cn/xw/hyyw_90/index.html'
               # , 'http://www.soa.gov.cn/xw/hyyw_90/index_2.html'
               #  ,'http://www.soa.gov.cn/xw/hyyw_90/index_3.html',
               #  'http://www.soa.gov.cn/xw/hyyw_90/index_4.html'
                }
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_pages, dont_filter=True)

    def parse_pages(self, response):
        try:
            print("parse_pages："+response.url)
            # '解析跳转到每篇文件链接'
            #print(response.body)
            #print("country:"+country)
            for news_url in response.xpath('//ul[@class="ul_liebiao1"]/li/a/@href').extract():
                news_url="http://www.soa.gov.cn/xw/hyyw_90"+str(news_url)[1:]
                print("news url:"+news_url)
                yield scrapy.Request(news_url,callback=self.parse_news, dont_filter=True)
        except Exception as error:
            log(error)

    def parse_news(self, response):
        try:
            print("parse:"+response.url)

            item = NewsItem()
            item['url'] = response.url

            item['country_code'] = "1"  # "".join(response.xpath('//*[@property="v:summary"]/text()').extract())
            item['country_name'] = "China"
            #print("country_code,country_name"+item['country_code']+item['country_name'])

            # image="".join(response.xpath('//section[@id="block-views-newsroom-page-block-1"]').extract())
            # if image:
            #     item['image']=image
            # else:
            #     item['image']=None
            item['source']="http://www.soa.gov.cn"
            item['image_urls'] = None
            item['content']="<br />".join(response.xpath('//div[@class="kuang_xiangqing"]/div/div[@class="TRS_Editor"]/p/font[name(..)!="img"][normalize-space()]').extract())
            #print("content"+item['content'])

            item['title']="".join(response.xpath('//div[@class="kuang_xiangqing"]/p[2]/text()').extract())#"".join(response.xpath('//div[@class="sf_colsOut contentIntroInternal"]/'
                                                # 'div[@class="sf_colsIn sf_1col_1in_100"]/h1/text()').extract())
            item['time']="".join(response.xpath('//div[@class="kuang_xiangqing"]/div[@class="subhead"]/text()').extract())
            item['crawled_time']=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            #print("title:" + item['title'])#print(item['title'])
            #print("time:" + item['time'])
            yield item
        except Exception as error:
            log(error)
