#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-02-08 22:36:52
# Project: Hupu_Json

from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    crawl_config = {
    }

    def __init__(self):
        self.start_url = 'https://nba.hupu.com/match/nba?offset=-'
        self.page = 0

    def on_start(self):
        while self.page < 4:
            self.crawl(self.start_url + str(self.page), callback=self.index_page)
            self.page += 1

    def index_page(self, response):
        for item in response.json['data']['list']:
            print(item['home_name'], item['home_score'], ':', item['away_score'], item['away_name'])

    @config(priority=2)
    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('title').text(),
        }