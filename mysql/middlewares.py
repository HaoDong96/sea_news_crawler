# -*-coding:utf-8-*-

from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from scrapy.conf import settings
# from scrapy.http.response import Response
from scrapy.http import HtmlResponse
import time
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from telnetlib import DO
import random
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware

class JavaScriptMiddleware(object):
    def __init__(self, user_agent=''):
        self.user_agent = user_agent
    def process_request(self, request, spider):
        #0_imo_org动态加载
        if (spider.name == "0_imo_org" and str(request.url).count("osssearchresults") ):
            print ("PhantomJS is starting...")
            driver = webdriver.PhantomJS(executable_path=settings['JS_BIN'])  # 指定使用的浏览器
            # driver = webdriver.Firefox()
            driver.get(request.url)
            body = driver.page_source
            return HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=request)

        # 0_worldcargonews动态加载翻页
        if(spider.name=="0_worldcargonews" and (str(request.url).count("search"))):
            print ("PhantomJS is starting...")
            driver = webdriver.PhantomJS(executable_path=settings['JS_BIN'])  # 指定使用的浏览器
            #driver = webdriver.Firefox()
            driver.get(request.url)
            time.sleep(5)
            # print(driver.page_source)
            # 翻页（因为是每天都运行此爬虫程序，所以没有必要翻页）
            worldcargonews_look_more = '//div[@class="aoci aos-searchc"]/button'
            for i in range(1,1):
                    try:
                        driver.find_element_by_xpath(worldcargonews_look_more).click()  # 数据由js来控制,点击后加载数据
                        time.sleep(2)
                        print("more page")
                    except:
                        print ("get news data failed")
            body = driver.page_source
            print ("final page")
            #print(driver.page_source)
            # driver.close()
            return HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=request)
            driver.close()

        #2_Brunei_jpm动态加载
        if (spider.name == "2_Brunei_jpm"):
            print ("PhantomJS is starting...")
            driver = webdriver.PhantomJS(executable_path=settings['JS_BIN'])  # 指定使用的浏览器
            # driver = webdriver.Firefox()
            driver.get(request.url)
            body = driver.page_source
            return HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=request)

        # 6_Malaysia_miti动态加载翻页
        if(spider.name=="6_Malaysia_miti" and str(request.url).count("search")):
            print ("PhantomJS is starting...")
            driver = webdriver.PhantomJS(executable_path=settings['JS_BIN'])  # 指定使用的浏览器
            #driver = webdriver.Firefox()
            driver.get(request.url)
            time.sleep(1)
            # 翻页
            Malaysia_miti_look_more = '//*[@id="more"]'
            if( str(request.url).count("search") ):
                 for i in range(1,1):
                    try:
                        driver.find_element_by_xpath(Malaysia_miti_look_more).click()  # 数据由js来控制,点击后加载数据
                        time.sleep(2)
                        #true_page = driver.page_source
                        print("more page")
                    except:
                        print ("get news data failed")
            body = driver.page_source
            print ("final page")
            #print(driver.page_source)
            # driver.close()
            return HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=request)
            driver.close()


        #10_Thailand_thaigov变语言
        if(spider.name=="10_Thailand_thaigov"):
            driver = webdriver.PhantomJS(executable_path=settings['JS_BIN'])  # 指定使用的浏览器
            # driver = webdriver.Firefox()
            driver.get(request.url)
            time.sleep(5)
            #变语言
            change_lang = driver.find_element_by_xpath('//*[@id="destop"]/div[@class="col-sm-8 col-md-8 remove-xs"]'
                                                       '/div[@class="col-xs-6 col-md-2 remove-xs"]/a[2]')  # .click()
            driver.execute_script("arguments[0].click();", change_lang);
            #time.sleep(20)
            WebDriverWait(driver, 30).until(lambda x: x.find_element_by_xpath("//*[contains(text(),'Change')]"))
            if((str(request.body).count("Thursday 01 January 1970"))):
                return;
            body = driver.page_source
            return HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=request)
            driver.close()




        # the default user_agent_list composes chrome,I E,firefox,Mozilla,opera,netscape
        # for more user agent strings,you can find it in http://www.useragentstring.com/pages/useragentstring.php
        user_agent_list = [ \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1" \
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11", \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6", \
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6", \
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1", \
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5", \
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5", \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3", \
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", \
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]
        #不需要动态加载的页面：
        ua = random.choice(user_agent_list)
        if ua:
          request.headers.setdefault('User-Agent', ua)


