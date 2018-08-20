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
    name = '0_imo_org'
    allowed_domains = ['imo.org']
    key_name = ['China','Brunei','Cambodia','Indonesia','Lao','Malaysia',
          'Myanmar','Philippine','Singapore','Thailand','Vietnam' ]
    # key_name=['China']
    base_url='http://www.imo.org/en/About/_layouts/15/osssearchresults.aspx?u=http%3A%2F%2Fwww%2Eimo%2Eorg%2Fen%2FAbout&k={key}'


    def start_requests(self):
        # 用for和字符串插入的方法构成关键字链接循环入口
        for key in self.key_name:
            url = self.base_url.format(key=key)
            yield scrapy.Request(url=url, callback=self.parse_pages, dont_filter=True, meta={"country": key})
            #print(url)

    def parse_pages(self, response):
        try:
            print("parse_pages："+response.url)
            # '解析跳转到每篇文件链接'
            #print(response.body)
            country = response.meta["country"]
            for news_url in response.xpath('//h3[@class="ms-srch-ellipsis"]/a/@href').extract():
                print("news url:"+news_url)
                yield scrapy.Request(news_url, callback=self.parse_news, dont_filter=True, meta={"country": country})
        except Exception as error:
            log(error)

    def parse_news(self, response):
        try:
            print("parse:" + response.url)
            country = response.meta["country"]
            #print(country)
            # print(response.body)
            item = NewsItem()
            item['url'] = response.url
            #
            if (country == 'China'):
                item['country_code'] = "1"  # "".join(response.xpath('//*[@property="v:summary"]/text()').extract())
                item['country_name'] = "China"
            elif (country == 'Brunei'):
                item['country_code'] = "2"  # "".join(response.xpath('//*[@property="v:summary"]/text()').extract())
                item['country_name'] = "Brunei"
            elif (country == 'Cambodia'):
                item['country_code'] = "3"  # "".join(response.xpath('//*[@property="v:summary"]/text()').extract())
                item['country_name'] = "Cambodia"
            elif (country == 'Indonesia'):
                item['country_code'] = "4"  # "".join(response.xpath('//*[@property="v:summary"]/text()').extract())
                item['country_name'] = "Indonesia"
            elif (country == 'Lao'):
                item['country_code'] = "5"  # "".join(response.xpath('//*[@property="v:summary"]/text()').extract())
                item['country_name'] = "Lao"
            elif (country == 'Malaysia'):
                item['country_code'] = "6"  # "".join(response.xpath('//*[@property="v:summary"]/text()').extract())
                item['country_name'] = "Malaysia"
            elif (country == 'Myanmar'):
                item['country_code'] = "7"  # "".join(response.xpath('//*[@property="v:summary"]/text()').extract())
                item['country_name'] = "Myanmar"
            elif (country == 'Philippine'):
                item['country_code'] = "8"  # "".join(response.xpath('//*[@property="v:summary"]/text()').extract())
                item['country_name'] = "Philippine"
            elif (country == 'Singapore'):
                item['country_code'] = "9"  # "".join(response.xpath('//*[@property="v:summary"]/text()').extract())
                item['country_name'] = "Singapore"
            elif (country == 'Thailand'):
                item['country_code'] = "10"  # "".join(response.xpath('//*[@property="v:summary"]/text()').extract())
                item['country_name'] = "Thailand"
            elif (country == 'Vietnam'):
                item['country_code'] = "11"  # "".join(response.xpath('//*[@property="v:summary"]/text()').extract())
                item['country_name'] = "Vietnam"
            # print("country_code,country_name" + item['country_code'] + item['country_name'])

            item['source']="http://www.imo.org"
            # image="".join(response.xpath('//section[@id="block-views-newsroom-page-block-1"]').extract())
            # if image:
            #     item['image']=image
            # else:
            #     item['image']=None
            item['image_urls'] = None
            content = str("".join(response.xpath('//*[@id="imo-pageLayout"]').extract()).replace("img "," "))
            # content.replace("img "," ")
            item['content']=content
            #print("content"+item['content'])

            item['title']="".join(response.xpath('//*[@id="imo-pageLayout"]/h1/text()').extract())
            item['time']=None#"".join(response.xpath('//*[@id="post-9384"]/div[2]/div/span[3]/text()').extract())
            item['crawled_time']=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            # print("title:" + item['title'])#print(item['title'])
            # print("time:" + item['time'])
            yield item
        except Exception as error:
            log(error)
