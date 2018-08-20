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
    name = '11_Vietnam_chinhphu'
    allowed_domains = ['cn.news.chinhphu.vn']
    # key_name = ['ocean','aquatic','marine ', 'fishery' ,  'harbor','warship','warcraft', 'fishing','coastal'
    #     , 'cargo+ship', 'cargo+vessel', 'cargo+boat'
    #         ,'maritime+policies','south+china+sea', 'blue+economy' ]
    key_name=['海洋','渔业','港口','船舶']
    # key_name = ['海洋']
    base_url={'http://cn.news.chinhphu.vn/Search.aspx?KeyWord={key}&Page=1'
              # ,'http://cn.news.chinhphu.vn/Search.aspx?KeyWord={key}&Page=2'
              #  ,'http://cn.news.chinhphu.vn/Search.aspx?KeyWord={key}&Page=3'
              # ,'http://cn.news.chinhphu.vn/Search.aspx?KeyWord={key}&Page=4'
              }


    def start_requests(self):
        # 用for和字符串插入的方法构成关键字链接循环入口
        for key in self.key_name:
         for url in self.base_url:
            url = url.format(key=key)
            yield scrapy.Request(url=url, callback=self.parse_pages, dont_filter=True)
    def parse_pages(self, response):
        try:
            print("parse_pages："+response.url)
            # '解析跳转到每篇文件链接'
            #print("".join(response.xpath('/html/body').extract()))
            for news_url in response.xpath('//div[@class="catItemBody"]/a/@href').extract():
                news_url="http://cn.news.chinhphu.vn"+news_url
                #print("news url:"+news_url)
                yield scrapy.Request(str(news_url),callback=self.parse_news, dont_filter=True)

        except Exception as error:
            log(error)

    def parse_news(self, response):
        try:
            print("parse:"+response.url)
            item = NewsItem()
            item['url'] = response.url
            item['country_code'] = "11"#"".join(response.xpath('//*[@property="v:summary"]/text()').extract())
            item['country_name']="Vietnam"

            item['image_urls']=None#"".join(response.xpath('//section[@id="block-views-newsroom-page-block-1"]').extract())

            item['content']= str("".join(response.xpath('//*[@id="aspnetForm"]/div[3]'
                                                        '/div[2]/div[2]/div[6]').extract()).replace('src="', 'src="http://cn.news.chinhphu.vn'))
            item['source']="http://cn.news.chinhphu.vn"
            item['title']="".join(response.xpath('//*[@id="ctl00_mainContent_bodyContent_lbHeadline"]/text()').extract())
            item['time']="".join(response.xpath('//*[@id="ctl00_mainContent_bodyContent_lbDate"]/text()').extract())
            item['crawled_time']=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            #print("title:" + item['title'])#print(item['title'])
            #print("time:" + item['time'])
            #print("content:" + item['content'])
            yield item
        except Exception as error:
            log(error)
