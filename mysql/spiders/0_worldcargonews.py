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

#动态翻页
class test_crawler(CrawlSpider):
    name = '0_worldcargonews'
    allowed_domains = ['worldcargonews.com']
    key_name = ['China','Brunei','Cambodia','Indonesia','Lao','Malaysia',
          'Myanmar','Philippine','Singapore','Thailand','Vietnam' ]
    # key_name=['China']#,'Singapore','Indonesia']
    base_url='https://www.worldcargonews.com/search?q={key}#q={key}&datefrom=01/01/2017'


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
            #print(country)
            for news_url in response.xpath('//h2[@class="aos-DS5-H2 aos-M0 aos-MB5px"]/a/@href').extract():
                news_url="https://www.worldcargonews.com/"+news_url
                #print("news url:"+news_url)
                yield scrapy.Request(news_url,callback=self.parse_news, dont_filter=True,meta={"country":country})
        except Exception as error:
            log(error)

    def parse_news(self, response):
        try:
            print("parse:"+response.url)
            country=response.meta["country"]
            print(country)
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


            item['source']="https://www.worldcargonews.com"



            content="".join(response.xpath('//div[@class="ao-Article ao-CrIb"]').extract())
            content.replace('<img src="/AcuCustom/Sitename/Icon/Icons/wcnIconLinkedIn.svg" alt="Linked In" title="Linked In" class="aos-DS5-Image aos-FL aos-MW100">'," ")
            content.replace('<img src="/AcuCustom/Sitename/Icon/Icons/wcnIconTwitter.svg" alt="Twitter" title="Twitter" class="aos-DS5-Image aos-FL aos-MW100">', ' ')
            content.replace('<img src="/AcuCustom/Sitename/Icon/Icons/wcnIconFB.svg" alt="Facebook" title="Facebook" class="aos-DS5-Image aos-FL aos-MW100">', '')
            content.replace('<img src="/AcuCustom/Sitename/Icon/Icons/wcnIconGoogleP.svg" alt="Google Plus" title="Google Plus" class="aos-DS5-Image aos-FL aos-MW100">', '')
            content.replace('<img src="/AcuCustom/Sitename/DAM/002/HHMC_STS_Delivered_to_Port_Louis.jpg" alt="HHMC STS cranes in Mauritius" title="HHMC STS cranes in Mauritius" class="aos-DS5-Image aos-W100">', '')


            item['content']=content
            # print("content"+item['content'])

            item['title']="".join(response.xpath('//div[@class="ao-Article ao-CrIb"]/h1/text()').extract())#"".join(response.xpath('//div[@class="sf_colsOut contentIntroInternal"]/'
                                                # 'div[@class="sf_colsIn sf_1col_1in_100"]/h1/text()').extract())
            item['time']="".join(response.xpath('//span[@class="aos-ArticleDate aos-MRXS4 aos-NM aos-FL aos-DF"]/text()').extract())
            item['crawled_time']=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

            item['image_urls'] = None




            yield item
        except Exception as error:
            log(error)
