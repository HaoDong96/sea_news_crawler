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
    name = '0_eworldship'
    allowed_domains = ['eworldship.com']
    key_name = ['中国','文莱','柬埔寨','印度尼西亚','老挝','马来西亚',
                '缅甸','菲律宾','新加坡','泰国','越南' ]
    # key_name=['中国']#,'新加坡','泰国']
    base_url='http://www.eworldship.com/app/search?typeid=1&q={key}&time=week'

    def start_requests(self):
        # 用for和字符串插入的方法构成关键字链接循环入口
        for key in self.key_name:
            url = self.base_url.format(key=key)
            yield scrapy.Request(url=url, callback=self.parse_pages, dont_filter=True,meta={"country":key})
            #print(url)

    def parse_pages(self, response):
        try:
            print("parse_pages："+response.url)
            # '解析跳转到每篇文件链接'
            #print(response.body)
            country=response.meta["country"]
            #print("country:"+country)
            for news_url in response.xpath('//div[@class="pt"]/a/@href').extract():
                news_url="http://www.eworldship.com"+news_url
                print("news url:"+news_url)
                yield scrapy.Request(news_url,callback=self.parse_news, dont_filter=True,meta={"country":country})
            #解析跳转到下一页
            # next_page="".join(response.xpath('//div[@id="pager"]/div[@class="pg"]/a[@class="next"]/@href').extract())
            # if(next_page):
            #   next_page="http://www.eworldship.com"+next_page
            #   print("next_page:"+next_page)
            #   yield scrapy.Request(next_page, callback=self.parse_pages, dont_filter=True, meta={"country": country})
        except Exception as error:
            log(error)

    def parse_news(self, response):
        try:
            print("parse:"+response.url)
            country=response.meta["country"]
            #print(response.body)
            item = NewsItem()
            item['url'] = response.url
            #
            if (country=='中国'):
              item['country_code'] = "1"#"".join(response.xpath('//*[@property="v:summary"]/text()').extract())
              item['country_name']="China"
            elif (country == '文莱'):
              item['country_code'] = "2"  # "".join(response.xpath('//*[@property="v:summary"]/text()').extract())
              item['country_name'] = "Brunei"
            elif (country=='柬埔寨'):
                item['country_code'] = "3"  # "".join(response.xpath('//*[@property="v:summary"]/text()').extract())
                item['country_name'] = "Cambodia"
            elif (country=='印度尼西亚'):
                item['country_code'] = "4"  # "".join(response.xpath('//*[@property="v:summary"]/text()').extract())
                item['country_name'] = "Indonesia"
            elif (country=='老挝'):
                item['country_code'] = "5"  # "".join(response.xpath('//*[@property="v:summary"]/text()').extract())
                item['country_name'] = "Lao"
            elif (country=='马来西亚'):
                item['country_code'] = "6"  # "".join(response.xpath('//*[@property="v:summary"]/text()').extract())
                item['country_name'] = "Malaysia"
            elif (country=='缅甸'):
                item['country_code'] = "7"  # "".join(response.xpath('//*[@property="v:summary"]/text()').extract())
                item['country_name'] = "Myanmar"
            elif (country=='菲律宾'):
                item['country_code'] = "8"  # "".join(response.xpath('//*[@property="v:summary"]/text()').extract())
                item['country_name'] = "Philippine"
            elif (country=='新加坡'):
                item['country_code'] = "9"  # "".join(response.xpath('//*[@property="v:summary"]/text()').extract())
                item['country_name'] = "Singapore"
            elif (country=='泰国'):
                item['country_code'] = "10"  # "".join(response.xpath('//*[@property="v:summary"]/text()').extract())
                item['country_name'] = "Thailand"
            elif (country=='越南'):
                item['country_code'] = "11"  # "".join(response.xpath('//*[@property="v:summary"]/text()').extract())
                item['country_name'] = "Vietnam"
            #print("country_code,country_name"+item['country_code']+item['country_name'])


            item['source']="http://www.eworldship.com"
            item['content']="".join(response.xpath('//*[@id="nArticle"]/div[3]').extract())
            #print("content"+item['content'])

            item['title']="".join(response.xpath('//*[@id="nArticle"]/h1/text()').extract())#"".join(response.xpath('//div[@class="sf_colsOut contentIntroInternal"]/'
                                                # 'div[@class="sf_colsIn sf_1col_1in_100"]/h1/text()').extract())
            item['time']="".join(response.xpath('//*[@id="artical_sth"]/p/span[1]/text()').extract())
            item['crawled_time']=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

            srcs = response.xpath('//*[@id="nArticle"]/div[@class="content"]/p/img/@src').extract()
            item['image_urls'] = srcs
            if (not srcs):
               item['image_urls']=None

            # print("title:" + item['title'])#print(item['title'])
            # print("time:" + item['time'])
            return item
        except Exception as error:
            log(error)
