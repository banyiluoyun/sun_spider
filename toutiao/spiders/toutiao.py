#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy,time,hashlib
from scrapy import Selector
from toutiao.items import ToutiaoItem
from scrapy.spiders import CrawlSpider, Rule
import requests,re,json
from scrapy_splash import SplashRequest
from urllib.parse import urlencode
from selenium import webdriver
import re
from lxml import etree
from scrapy import Spider
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.utils.project import get_project_settings

# 创建一个Spider，必须继承 scrapy.Spider 类
class comicspider(scrapy.Spider):
    name = 'tt'
    allowed_domains=['www.toutiao.com']
    start_urls=['https://www.toutiao.com',
                'https://www.toutiao.com/ch/news_tech/',
                'https://www.toutiao.com/ch/news_entertainment/',
                'https://www.toutiao.com/ch/news_game/',
                'https://www.toutiao.com/ch/news_sports/',
                'https://www.toutiao.com/ch/news_finance/',
                'https://www.toutiao.com/ch/funny/',
                'https://www.toutiao.com/ch/news_military/',
                'https://www.toutiao.com/ch/news_fashion/',
                'https://www.toutiao.com/ch/news_discovery/',
                'https://www.toutiao.com/ch/news_regimen/',
                'https://www.toutiao.com/ch/news_history/',
                'https://www.toutiao.com/ch/news_world/',
                'https://www.toutiao.com/ch/news_travel/',
                'https://www.toutiao.com/ch/news_baby/',
                'https://www.toutiao.com/ch/news_essay/',
                'https://www.toutiao.com/ch/news_food/',]

    headers = {
        'Connection': 'keep-alive',
        'Host': 'www.toutiao.com',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'
    }

    # 进入浏览器设置
    options = webdriver.ChromeOptions()
    # 设置中文
    # options.add_argument('lang=zh_CN.UTF-8')
    # options.set_headless()
    options.add_argument(
        'user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"')
    # brower = webdriver.Chrome(chrome_options=options)
    options.add_argument('lang=zh_CN.UTF-8')
    options.add_argument('--disable-gpu')
    options.add_argument('--headless')
    options.add_argument(
        'user-agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36"')
    brower = webdriver.Chrome(executable_path="/home/lis/Downloads/chromedriver", chrome_options=options)
    ajax_url_base = 'https://www.toutiao.com/api/pc/feed/?'
    # for url in start_urls:
    #     start_url = url
    #     print(url)
    def start_requests(self):
        yield SplashRequest(url=self.start_urls[0],callback=self.sub_nav, splash_headers=self.headers,args={'wait':0.5},)
    # yield scrapy.Request(url=self.start_urls[0],callback=self.sub_nav,headers=self.headers,dont_filter=True)

    def sub_nav(self, response):
        page = Selector(response)
        # print(page)

        # print(response.text)
        # 所有子标签的url
        sub_nav_tips1=page.xpath('//div[@class="channel"]/ul/li/a/@href').extract()
        # print('栏目名称11111111111111111')
        sub_nav_tips1.pop()
        # print(sub_nav_tips1)

        sub_nav_tips1.append('/ch/news_military/')
        sub_nav_tips1.append('/ch/news_fashion/')
        sub_nav_tips1.append('/ch/news_discovery/')
        sub_nav_tips1.append('/ch/news_regimen/')
        sub_nav_tips1.append('/ch/news_history/')
        sub_nav_tips1.append('/ch/news_world/')
        sub_nav_tips1.append('/ch/news_travel/')
        sub_nav_tips1.append('/ch/news_baby/')
        sub_nav_tips1.append('ch/news_essay/')
        sub_nav_tips1.append('/ch/news_food/')

        # print(sub_nav_tips1)
        del sub_nav_tips1[:2],sub_nav_tips1[-1],sub_nav_tips1[1]
        sub_nav_tips2=page.xpath('//div[@class="channel-more-layer"]/ul/li/a/@href').extract()
        sub_nav_tips=sub_nav_tips1+sub_nav_tips2

        sub_nav_tips.append('/ch/news_military/')
        sub_nav_tips.append('/ch/news_fashion/')
        sub_nav_tips.append('/ch/news_discovery/')
        sub_nav_tips.append('/ch/news_regimen/')
        sub_nav_tips.append('/ch/news_history/')
        sub_nav_tips.append('/ch/news_world/')
        sub_nav_tips.append('/ch/news_travel/')
        sub_nav_tips.append('/ch/news_baby/')
        sub_nav_tips.append('ch/news_essay/')
        sub_nav_tips.append('/ch/news_food/')

        #子标签的名字
        sub_names1=page.xpath('//div[@class="channel"]/ul/li/a/span/text()').extract()
        del sub_names1[:2], sub_names1[-1],sub_names1[1]
        sub_names2=page.xpath('//div[@class="channel-more-layer"]/ul/li/a/span/text()').extract()

        sub_names=sub_names1+sub_names2

        # 每个子标签遍历
        try:
            for i in range(0,len(sub_nav_tips)):
                # time.sleep(0.5)
                items=[]
                # 请求子标签页面
                # print(sub_nav_tips1[i])
                if sub_nav_tips1[i]== 'https://www.dcdapp.com/?zt=tt_pc_home_channel':
                    pass
                else:
                    self.brower.get('https://www.toutiao.com' + sub_nav_tips[i])
                    # 返回秒时间戳
                    now = round(time.time())
                    # 获取signature加密数据
                    signature = self.brower.execute_script('return TAC.sign(' + str(now) + ')')
                    # print(signature)
                    # 获取cookie
                    cookie = self.brower.get_cookies()
                    cookie = [item['name'] + "=" + item['value'] for item in cookie]
                    cookiestr = '; '.join(item for item in cookie)
                    # print(cookiestr)

                    header1 = {
                        'Host': 'www.toutiao.com',
                        'User-Agent': '"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"',
                        # 'Referer': 'https://www.toutiao.com/ch/news_hot/',
                        "Cookie": cookiestr
                    }

                    send_data = {
                        'category': sub_nav_tips[i][4:-1],
                        'utm_source': 'toutiao',
                        'widen': '1',
                        'max_behot_time': now,
                        '_signature': signature
                    }
                    # 拼接ajax URL
                    url = self.ajax_url_base + urlencode(send_data)
                    print(url)
                    html = requests.get(url, headers=header1, verify=False)
                    # 返回json数据，解析
                    # print('11123132132132131232132131231',json.loads(html.text))
                    try:
                        json_datas = json.loads(html.text)['data']
                        # print(json_datas)
                        for json_data in json_datas:
                            item = ToutiaoItem()
                            # print(type(json_data))
                            item['title']=json_data['title']
                            # 有的字段为空
                            try:item['source_url']='https://www.toutiao.com/a'+json_data['source_url'][7:]
                            except: item['source_url']=''
                            try:item['abstract']=json_data['abstract']
                            except: item['abstract']=''
                            try:item['source']=json_data['source']
                            except: item['source']=''
                            try:item['tag']=json_data['tag']
                            except:item['tag']=''
                            try:item['chinese_tag']=json_data['chinese_tag']
                            except: item['chinese_tag']='无标签类别'
                            item['news_class']=sub_names[i]
                            yield item
                    except Exception as e:
                        print('数据处理模块报错')
        except Exception as e:
            print("栏目报错，请检查栏目")
            pass
        self.brower.quit()


if __name__ == "__main__":
    process = CrawlerProcess(get_project_settings())
    process.crawl('tt')
    time.sleep(20)
    process.start(stop_after_crawl = False)