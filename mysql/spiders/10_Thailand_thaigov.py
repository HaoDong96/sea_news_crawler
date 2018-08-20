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
#from selenium import webdriver

class test_crawler(CrawlSpider):
    name = '10_Thailand_thaigov'
    allowed_domains = ['thaigov.go.th']
    key_name = ['ocean','aquatic','marine', 'fish' ,'warship','coastal']
    # key_name=['ocean']
    base_url='http://www.thaigov.go.th/search?keyword={key}'


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
            for news_url in response.xpath('//div[@class="col-xs-12 col-sm-9 col-md-10 news-2"]/p/a/@href').extract():
                print("news url:" + news_url)
                yield scrapy.Request(str(news_url),callback=self.parse_news, dont_filter=True)
        except Exception as error:
            log(error)

    def parse_news(self, response):
        try:
            print("parse:"+response.url)
            #print(str(response.css('.main-content *').extract()))
            #print("".join(response.xpath('/html/body').extract()))
            item = NewsItem()
            item['url'] = response.url
            item['country_code'] = "10"#"".join(response.xpath('//*[@property="v:summary"]/text()').extract())
            item['country_name']="Thailand"
            #content="".join(response.xpath('/html/body').extract())
            #content = re.sub('div class="col-sm-12 hidden-print"[\w\W]+sidebar', '', content).strip()
            # srcs="".join(response.xpath('//div[@class="col-xs-12 col-sm-6 padding-sm1 news-2"]/figure/img/@src').extract())
            item['image_urls'] = None

            #print("image:"+item['image'])
            item['content']="".join(response.xpath('//div[@class="border-normal clearfix"]').extract())
            #print("content:"+item['content'])
            item['source']="http://www.thaigov.go.th"
            item['title']="".join(response.xpath('//div[@class="col-xs-12 col-sm-6 padding-sm1 news-2"]/h3[@class="news-1 Circular color2"]/text()').extract())
            #print("title:" + item['title'])
            item['time']="".join(response.xpath('//*[@id="banner-group"]/div/div/div/div[1]/div[2]/div[1]/p[1]/span[2]/text()').extract())
            #print("time:" + item['time'])
            item['crawled_time']=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            #print(item['title'])
            yield item
        except Exception as error:
            log(error)
