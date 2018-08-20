# # -*- coding: utf-8 -*-
#
# # Scrapy settings for mysql project
# #
# # For simplicity, this file contains only settings considered important or
# # commonly used. You can find more settings consulting the documentation:
# #
# #     http://doc.scrapy.org/en/latest/topics/settings.html
# #     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
# #     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#
BOT_NAME = 'mysql'

#开启图片管道
ITEM_PIPELINES = {
    'mysql.pipelines.MyImagesPipeline': 1,
    'mysql.pipelines.NewsPipeline': 301,
}
DOWNLOAD_TIMEOUT = 500
#将ＩＭＡＧＥＳ＿ＳＴＯＲＥ设置为一个有效的文件夹，用来存储下载的图片．否则管道将保持禁用状态，即使你在ＩＴＥＭ＿ＰＩＰＥＬＩＮＥＳ设置中添加了它．
IMAGES_STORE = 'E:\\apache-tomcat-8.5.29\\webapps\\sea_news_images'


SPIDER_MODULES = ['mysql.spiders']
NEWSPIDER_MODULE = 'mysql.spiders'


MYSQL_HOST = 'chinaaseanocean.mysql.rds.aliyuncs.com'
MYSQL_DBNAME = 'chinaaseanocean'
MYSQL_USER = 'chinaaseanocean'
MYSQL_PASSWD = 'x3m0u8X#M)U*'

DOWNLOAD_DELAY = 1

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'mysql.middlewares.JavaScriptMiddleware': 543
}
COMMANDS_MODULE = 'mysql.commands'#crawlall
#LOG_FILE="log.txt"

#phantomjs的文件路径
JS_BIN="C:\\Users\\Administrator\\Desktop\\sea_news_crawler\\venv\\Scripts\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe"

# LOGIN_TYPE="myCrawl"


#反爬机制
ROBOTSTXT_OBEY = False
#设置取消Cookes
COOKIES_ENABLED = False
#设置用户代理值,随便浏览一个网页，按F12 -> Network -> F5，随便点击一项，你都能看到有 User-agent 这一项，将这里面的内容拷贝就可以。
# USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
AUTOTHROTTLE_ENABLED = False
CONCURRENT_REQUESTS=500
DOWNLOAD_TIMEOUT = 180
