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
    name = '0_seatrade_cruise'
    allowed_domains = ['seatrade-cruise.com']
    key_name = ['China','Brunei','Cambodia','Indonesia','Lao','Malaysia',
          'Myanmar','Philippine','Singapore','Thailand','Vietnam' ]
    # key_name=['China']
    base_url={'http://www.seatrade-cruise.com/search.html?q={key}'
              # ,'http://www.seatrade-cruise.com/search.html?q={key}&start=20',
              # 'http://www.seatrade-cruise.com/search.html?q={key}&start=40',
              # 'http://www.seatrade-cruise.com/search.html?q={key}&start=60'
              }


    def start_requests(self):
        # 用for和字符串插入的方法构成关键字链接循环入口
        for key in self.key_name:
          for url in self.base_url:
            url = url.format(key=key)
            yield scrapy.Request(url=url, callback=self.parse_pages, dont_filter=True,meta={"country":key})
            #print(url)

    def parse_pages(self, response):
        try:
            print("parse_pages："+response.url)
            # '解析跳转到每篇文件链接'
            #print(response.body)
            country=response.meta["country"]
            #print(country)
            for news_url in response.xpath('//ul[@class="search-results list-striped"]/li/h4/a/@href').extract():
                news_url="http://www.seatrade-cruise.com"+news_url
                print(news_url)
                yield scrapy.Request(news_url,callback=self.parse_news, dont_filter=True,meta={"country":country})
        except Exception as error:
            log(error)

    def parse_news(self, response):
        try:
            print("parse:"+response.url)
            country=response.meta["country"]
            #print(country)
            #print(response.body)
            item = NewsItem()
            item['url'] = response.url
            #
            if (country=='China'):
              item['country_code'] = "1"#"".join(response.xpath('//*[@property="v:summary"]/text()').extract())
              item['country_name']="China"
            elif (country == 'Brunei'):
              item['country_code'] = "2"  # "".join(response.xpath('//*[@property="v:summary"]/text()').extract())
              item['country_name'] = "Brunei"
            elif (country=='Cambodia'):
                item['country_code'] = "3"  # "".join(response.xpath('//*[@property="v:summary"]/text()').extract())
                item['country_name'] = "Cambodia"
            elif (country=='Indonesia'):
                item['country_code'] = "4"  # "".join(response.xpath('//*[@property="v:summary"]/text()').extract())
                item['country_name'] = "Indonesia"
            elif (country=='Lao'):
                item['country_code'] = "5"  # "".join(response.xpath('//*[@property="v:summary"]/text()').extract())
                item['country_name'] = "Lao"
            elif (country=='Malaysia'):
                item['country_code'] = "6"  # "".join(response.xpath('//*[@property="v:summary"]/text()').extract())
                item['country_name'] = "Malaysia"
            elif (country=='Myanmar'):
                item['country_code'] = "7"  # "".join(response.xpath('//*[@property="v:summary"]/text()').extract())
                item['country_name'] = "Myanmar"
            elif (country=='Philippine'):
                item['country_code'] = "8"  # "".join(response.xpath('//*[@property="v:summary"]/text()').extract())
                item['country_name'] = "Philippine"
            elif (country=='Singapore'):
                item['country_code'] = "9"  # "".join(response.xpath('//*[@property="v:summary"]/text()').extract())
                item['country_name'] = "Singapore"
            elif (country=='Thailand'):
                item['country_code'] = "10"  # "".join(response.xpath('//*[@property="v:summary"]/text()').extract())
                item['country_name'] = "Thailand"
            elif (country=='Vietnam'):
                item['country_code'] = "11"  # "".join(response.xpath('//*[@property="v:summary"]/text()').extract())
                item['country_name'] = "Vietnam"
            #print("country_code,country_name"+item['country_code']+item['country_name'])


            item['source']="http://www.seatrade-cruise.com"

            item['content']="".join(response.xpath('//*[@id="k2Container"]/div[@class="itemBody"]/div[@class="contentBlock"]').extract())
            #print("content"+item['content'])

            item['title']="".join(response.xpath('//*[@id="k2Container"]/div[@class="itemHeader"]/h1/text()').extract())
            item['time']="".join(response.xpath('//*[@id="k2Container"]/div[@class="itemBody"]/span/text()').extract())
            item['crawled_time']=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))


            srcs = "http://www.seatrade-cruise.com"+"".join(response.xpath('//*[@id="k2Container"]/div[@class="itemBody"]/div[@class="itemImageBlock"]/span[@class="itemImage"]/a/@href').extract())
            item['image_urls'] = srcs.split()
            if (not srcs):
                item['image_urls'] = None


            # print("title:" + item['title'])#print(item['title'])
            # print("time:" + item['time'])
            yield item
        except Exception as error:
            log(error)
