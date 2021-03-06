#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-01-28 13:38:59
# Project: taobaoMMcrawler
import os
from pyspider.libs.base_handler import *
import logging

PAGE_START = 1
PAGE_END = 30
DIR_PATH = '/Users/tongxiaoyu/Documents/Picture/PySpider_Taobao3'
result = '/Users/tongxiaoyu/Documents/Picture/PySpider_Taobao3/result.txt'
result2 = '/Users/tongxiaoyu/Documents/Picture/PySpider_Taobao3/resul2.txt'


class Handler(BaseHandler):
    crawl_config = {
    }

    def __init__(self):
        self.base_url = 'https://mm.taobao.com/json/request_top_list.htm?page='
        self.page_num = PAGE_START
        self.total_num = PAGE_END
        self.saveObj = save()

    def on_start(self):
        while self.page_num <= self.total_num:
            url = self.base_url + str(self.page_num)
            self.crawl(url, callback=self.index_page, save={'pagnum': self.page_num})
            self.page_num += 1

    def index_page(self, response):
        count = 1
        for each in response.doc('.lady-name').items():

            with open(result2, 'a') as f:
                f.write('into page > ' + str(response.save['pagnum']) + ' person' + str(count) + '\n')
                count += 1

            self.crawl(each.attr.href, callback=self.detail_page, fetch_type='js')

    def detail_page(self, response):
        domain = response.doc('.mm-p-domain-info li > span').text()
        mmName = response.doc('.mm-p-model-info-left-top dd > a').text()
        if domain:
            page_url = 'https:' + domain
            brief = response.doc('.mm-p-base-info').text()

            # ！！！！！！！！！！
            # 回调函数是异步的，所不能直接在imaeg_page()方法中引用brief，要用save字典传递
            self.crawl(page_url, callback=self.image_page, save={'brief': brief})
            return 'into > ' + mmName + " 's detail page"
        else:
            with open(result, 'a') as f:
                f.write(mmName + '  have not image page\n')
            return mmName + ' have not image page'

    # 十天内忽视同一请求
    @config(age=10*24*60*60)
    def image_page(self, response):
        name = response.doc('.mm-p-model-info-left-top dd > a').text()
        people_dir_path = self.saveObj.mkDir(name)
        if people_dir_path:
            count = 1
            self.saveObj.saveBrief(response.save['brief'], people_dir_path, name)
            for img in response.doc('.mm-aixiu-content img').items():
                url = img.attr.src
                if url:
                    extension = self.saveObj.getExtension(url)
                    filename = name + str(count) + '.' + extension
                    count += 1
                    # self.crawl(url, callback=self.saveImg,
                    #            save={'people_dir_path': people_dir_path, 'filename': filename})
        with open(result, 'a') as f:
            f.write('begin save > ' + name + " 's image\n")
        return 'begin save > ' + name + " 's image"

    def saveImg(self, response):
        content = response.content
        people_dir_path = response.save['people_dir_path']
        filename = response.save['filename']
        filepath = people_dir_path + '/' + filename
        self.saveObj.saveImg(content, filepath)


class save:
    def __init__(self):
        self.DIR_PATH = DIR_PATH
        if not self.DIR_PATH.endswith('/'):
            self.DIR_PATH = self.DIR_PATH + '/'
        if not os.path.exists(self.DIR_PATH):
            os.makedirs(self.DIR_PATH)

    def mkDir(self, name):
        people_dir_path = os.path.join(self.DIR_PATH, name.strip())
        if not os.path.exists(people_dir_path):
            os.makedirs(people_dir_path)
            return people_dir_path
        else:
            return people_dir_path

    def saveImg(self, content, path):
        with open(path, 'wb') as f:
            f.write(content)

    def saveBrief(self, content, dir_path, name):
        filename = dir_path + '/' + name + '.txt'
        with open(filename, 'w') as f:
            f.write(content)

    def getExtension(self, url):
        extension = url.split('.')[-1]
        return extension
