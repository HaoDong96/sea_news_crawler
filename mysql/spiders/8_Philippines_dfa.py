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
    name = '8_Philippines_dfa'
    allowed_domains = ['dfa.gov.ph']
    key_name = ['ocean','aquatic','marine ', 'fishery' ,  'harbor','warship','warcraft', 'fishing','coastal'
        , 'cargo+ship', 'cargo+vessel', 'cargo+boat'
            ,'maritime+policies','south+china+sea', 'blue+economy' ]
    # key_name=['ocean']
    base_url='https://www.dfa.gov.ph/search?searchword={key}&ordering=newest&searchphrase=all&limit=20&areas[0]=categories&areas[1]=contacts&areas[2]=content'


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
            for news_url in response.xpath('//dl[@class="search-results"]/dt[@class="result-title"]/a/@href').extract():
                news_url="https://www.dfa.gov.ph"+news_url
                print("news url:" + news_url)
                yield scrapy.Request(str(news_url),callback=self.parse_news, dont_filter=True)
        except Exception as error:
            log(error)

    def parse_news(self, response):
        try:
            print("parse:"+response.url)
            #print(str(response.css('.main-content *').extract()))

            item = NewsItem()
            item['url'] = response.url
            item['country_code'] = "8"
            item['country_name']="Philippines"

            #content="".join(response.xpath('/html/body').extract())
            #content = re.sub('div class="col-sm-12 hidden-print"[\w\W]+sidebar', '', content).strip()
            # image="".join(response.xpath('//div[@class="item-page"]/div[@itemprop="articleBody"]/p/img').extract())
            # if image:
            #     item['image']=image
            # else:
            srcs = "https://www.dfa.gov.ph"+"".join(response.xpath('//div[@class="item-page"]/div[@itemprop="articleBody"]/p/img/@src').extract())
            item['image_urls'] = srcs.split()
            #print("image:"+item['image'])
            item['content']="<br /><br />".join(response.xpath('//div[@class="item-page"]/div[@itemprop="articleBody"]/p/span').extract()).replace('src="','src="https://www.dfa.gov.ph')
            #print("content:"+item['content'])
            item['source']="https://www.dfa.gov.ph"
            item['title']="".join(response.xpath('//*[@id="banner"]/div/div/header/h1/text()').extract())
            #print("title:" + item['title'])
            item['time']="".join(response.xpath('//*[@id="content"]/div[2]/div[2]/dl/dd[2]/time/text()').extract())
            #print("time:" + item['time'])
            item['crawled_time']=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            #print(item['title'])
            yield item
        except Exception as error:
            log(error)
