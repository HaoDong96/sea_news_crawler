# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.org/en/latest/topics/items.html

from scrapy import Item, Field

class NewsItem(Item):
    country_code=Field()
    country_name = Field()
    url = Field()
    title = Field()
    time = Field()
    image_urls = Field()
    image_paths=Field()
    image= Field()
    content=Field()
    source = Field()
    click_count= Field()
    crawled_time= Field()





