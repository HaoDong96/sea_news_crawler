# coding:utf-8
import subprocess
import schedule
from scrapy import cmdline
import time
# cmdline.execute("scrapy crawl 0_worldcargonews".split())
#
def crawl_work():
    # cmdline.execute('scrapy crawl my_spider'.split()) # 不要用自带的cmdline
    subprocess.Popen('scrapy crawlall') # Execute a child program in a new process.

if __name__=='__main__':
    crawl_work()
    schedule.every(300).minutes.do(crawl_work)
    while True:
        schedule.run_pending()
        time.sleep(1)