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
    name = '9_Singapore_pmo'
    allowed_domains = ['pmo.gov.sg']
    key_name = ['ocean','aquatic','marine ', 'fishery' ,  'harbor','warship','warcraft',
    'fishing','coastal'
, 'cargo+ship', 'cargo+vessel', 'cargo+boat'
            ,'maritime+policies','south+china+sea', 'blue+economy' ]
    # key_name=['ocean']
    base_url='http://www.pmo.gov.sg/newsroom?keywords={key}'


    def start_requests(self):
        # 用for和字符串插入的方法构成关键字链接循环入口
        for key in self.key_name:
            url = self.base_url.format(key=key)
            yield scrapy.Request(url=url, callback=self.parse_pages, dont_filter=True)
    def parse_pages(self, response):
        try:
            print("parse_pages："+response.url)
            # '解析跳转到每篇文件链接'
            #print("".join(response.xpath('/html/body').extract()))
            for news_url in response.xpath('//div[@class="snippet"]/'
            'div[@class="snippet-content half-width"]/h2/a[2]/@href').extract():
                # i=i+1
                # if(i==1 or i>4):
                #     continue
                #news_url= "".join(re.findall(r"/url\?q=(.+?)&sa=U", str(old_news_url)))
                news_url="http://www.pmo.gov.sg"+news_url
                print("news url:"+news_url)
                yield scrapy.Request(str(news_url),callback=self.parse_news, dont_filter=True)
          # '解析跳转到搜索结果的下一页'
            next_page="".join(response.xpath('//div[@class="pagination-container"]'
            '/div[@class="text-center"]/ul[@class="pagination"]/li[@class="next"]/a/@href').extract())
            if next_page :
              next_page="http://www.pmo.gov.sg"+str(next_page)
              #print("next_page ："+next_page)
              requesturl = next_page
              yield scrapy.Request(requesturl,  callback=self.parse_pages, dont_filter=True)
        except Exception as error:
            log(error)

    def parse_news(self, response):
        try:
            print("parse:"+response.url)
            item = NewsItem()
            item['url'] = response.url
            item['country_code'] = "9"
            item['country_name']="Singapore"
            srcs = "".join( response.xpath('//*[@id="block-views-newsroom-page-block-1"]'
                                           '/div/div/div/div/div[2]/img/@src').extract())
            item['image_urls'] = srcs.split()


            item['content']="<br /><br />".join(response.xpath('/div[@class="row qna"]'
                                          '/div/p/text()[name(..)!="img"]').extract())
            item['source']="http://www.pmo.gov.sg"
            item['title']="".join(response.xpath('//div[@class="breadcrumb"]'
                              '/span[@class="inline even last"]/a/text()').extract())
            item['time']="".join(response.xpath('//div[@class="col-sm-12 col-md-12"]'
                              '/div[@class="meta-table"]/text()').extract())
            item['crawled_time']=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            yield item
        except Exception as error:
            log(error)
