# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from scrapy import log
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.http import Request
from mysql import settings

class MyImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if (item['image_urls']):
          for image_url in item['image_urls']:
              yield Request(image_url)

    def item_completed(self, results, item, info):
        image_path = [x['path'] for ok, x in results if ok]
        item['image_paths'] = image_path
        if not image_path:
            item['image_paths'] = None
            print('Item contains no images')
        return item


class NewsPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            port=3306,
            charset='utf8',
            use_unicode=True)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
            try:
                #查找表中有无现在正在爬的url
                self.cursor.execute("""select * from sea_news where url = %s""", item["url"])
                ret = self.cursor.fetchone()
                print("test pipelines")
                #如果没有，就插入
                if not ret:
                  if(item['title'] ):
                   if(len(str(item['content']))>5):
                    click_count=0
                    item['click_count']=str(click_count)
                    self.cursor.execute(
                        """insert into sea_news(country_code,country_name,url,title,time,image_paths,content,source,click_count,crawled_time)
                          value (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                        (
                            item['country_code'],
                            item['country_name'],
                            item['url'],
                            item['title'],
                            item['time'],
                            item['image_paths'],
                            item['content'],
                            item['source'],
                            item['click_count'],
                            item['crawled_time']
                        )
                    )

                self.connect.commit()
            except Exception as error:
                log(error)
            return item


