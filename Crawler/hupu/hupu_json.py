#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-02-08 22:36:52
# Project: Hupu_Json

from pyspider.libs.base_handler import *

page = 0


class Handler(BaseHandler):
    crawl_config = {
    }

    def __init__(self):
        self.start_url = 'https://nba.hupu.com/match/nba?offset=-'

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl(self.start_url + str(page), callback=self.index_page, save={'page': page})

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        page = response.save['page']
        print(response.text)
        page += 1
        if page < 3:
            self.crawl(self.start_url + str(page), callback=self.index_page, save={'page': page})

    @config(priority=2)
    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('title').text(),
        }