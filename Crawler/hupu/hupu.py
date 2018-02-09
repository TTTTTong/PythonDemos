#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-02-04 22:19:52
# Project: Hupu

from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    crawl_config = {
    }

    def __init__(self):
        self.team = []
        self.score = []

    def on_start(self):
        self.crawl('https://nba.hupu.com/', callback=self.index_page, fetch_type='js')

    def index_page(self, response):

        for each in response.doc(
                'div.content-wrap > div.nba-sidebar-wrap > div.nba-matchList > div.matchlist > '
                'div.match-box div#J-t-game .teamname').items():
            self.team.append(each.text())

        for each in response.doc(
                'div.content-wrap > div.nba-sidebar-wrap > div.nba-matchList > div.matchlist > '
                'div.match-box div#J-t-game .pknum').items():
            self.score.append(each.text())

        result = list(zip(self.team, self.score))
        for a, b in zip(result[0::2], result[1::2]):
            print(a[0], '', a[1], ':', b[1], '', b[0])

        self.crawl(response.doc('.match-nbalist.active .nbaPrevDay'), callback=self.index_page, fetch_type='js')

    @config(priority=2)
    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('title').text(),
        }