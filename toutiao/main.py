# -*- coding: utf-8 -*-
import subprocess
import schedule
import time
import datetime
from multiprocessing import Process
from scrapy import cmdline
import logging
def crawl_work():
    # subprocess.Popen('scrapy crawl it')
    print('-'*100)
    args = ["scrapy", "crawl", 'tt']
    while True:
        start = time.time()
        p = Process(target=cmdline.execute, args=(args,))
        p.start()
        p.join()
        logging.debug("### use time: %s" % (time.time() - start))
if __name__=='__main__':
    print('*'*10+'开始执行定时爬虫'+'*'*10)
    schedule.every(1).minutes.do(crawl_work)
    print('当前时间为{}'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    print('*' * 10 + '定时爬虫开始运行' + '*' * 10)
    while True:
        schedule.run_pending()
        time.sleep(10)






