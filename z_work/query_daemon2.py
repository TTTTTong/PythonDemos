#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb
import commands
import redis
import time
import logging
import logging.config
import os
from threading import Thread

logging.config.fileConfig(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'log.conf'))
logger = logging.getLogger('monitor')
logger.info('start monitor daemon')

# 多线程版本, ticker、kline、trade、depth各占一个线程,某项重启等待时不影响其他项


def get_mysqlcur():
    conn = MySQLdb.connect(host='rm-j6ccb77fan1q3p0n8.mysql.rds.aliyuncs.com',
                           user='rshvip', passwd='Aa112255', db='coindata')
    cur = conn.cursor()
    return cur


# 从数据库获取各项最新值
def query_ticker(exchange_id, symbol):
    cur_ticker = get_mysqlcur()
    sql = "SELECT `close` FROM `market_ticker` WHERE `exchange_id` = %s AND `symbol` = %s"
    cur_ticker.execute(sql, args=(exchange_id, symbol))
    res = cur_ticker.fetchone()
    if res is None:
        logger.info('query_ticker is None, return 0, exchanged_id is:%s,symbol is:%s' % (exchange_id, symbol))
        res = 0
    else:
        res = res[0]
    cur_ticker.close()
    return res


def query_kline(excahnge_id, symbol):
    cur_kline = get_mysqlcur()
    sql = "SELECT `time` FROM `market_kline` WHERE `exchange_id`=%s AND `symbol`=%s AND" \
          " `period`=1 ORDER BY `time` DESC LIMIT 1"
    cur_kline.execute(sql, args=(excahnge_id, symbol))
    res = cur_kline.fetchone()
    if res is None:
        logger.info('query_kline is None, return 0, exchanged_id is:%s,symbol is:%s' % (excahnge_id, symbol))
        res = 0
    else:
        res = res[0]
    cur_kline.close()
    return res


def query_trade(exchange_id, symbol):
    cur_trade = get_mysqlcur()
    sql = "SELECT `time` FROM `market_history_trade` WHERE `exchange_id`=%s AND " \
          "`symbol`=%s ORDER BY `time` DESC LIMIT 1"
    cur_trade.execute(sql, args=(exchange_id, symbol))
    res = cur_trade.fetchone()
    if res is None:
        logger.info('query_trade is None, return 0, exchanged_id is:%s,symbol is:%s' % (exchange_id, symbol))
        res = 0
    else:
        res = res[0]
    cur_trade.close()
    return res


def query_depth(exchange_id, symbol):
    rd = redis.StrictRedis(host='r-j6c9942d609540d4.redis.rds.aliyuncs.com', port=6379, db=0, password='Jr12345678')
    key = str(exchange_id) + ':' + str(symbol) + ':asks'
    result_dict = rd.hgetall(key)
    return result_dict


# 重启服务
def restart(name):
    command = 'pm2 restart ' + name
    commands.getstatusoutput(command)
    logger.error('restart:%s' % name)


# 将时间戳转换为(时:分:秒)
def format_time(timestamp):
    return time.strftime('%H:%M:%S', time.localtime(timestamp))


# 各项的处理函数, 决定是否重启对应服务
# ticket
def ticker_handle():
    result_dict = {}
    init_result = [0, 0, 1]
    for item in item_list:
        # 为每个交易所的每个交易对保存查询结果
        # 每个结果为包含三个元素的list，三次一样则重启，[0, 0, 1]为初始指定值
        result_dict[item[1]+'_'+item[2]] = init_result

    while True:
        is_restart = False
        for item in item_list:
            # 每个交易所的每个交易对的三次查询结果
            symbol_rst = result_dict[item[1]+'_'+item[2]]
            symbol_rst[0], symbol_rst[1] = symbol_rst[1], symbol_rst[2]
            symbol_rst[2] = query_ticker(item[0], item[1])
            logger.info('item is: %s,last three results: %s, %s, %s' % (str(item[0])+'_'+str(item[1])+'_'+str(item[2]),
                                                                       symbol_rst[0], symbol_rst[1], symbol_rst[2]))
            if symbol_rst[0] == symbol_rst[1] == symbol_rst[2]:
                restart(item[2] + '_ticker')
                logger.info('begin sleep 120s after restart %s_ticket' % item[2])
                time.sleep(120)
                is_restart = True
                logger.info('finish sleep 120s after restart %s_ticket' % item[2])
        if not is_restart:    
            logger.info('all ticker is normal, sleep 30s before next query' )
            time.sleep(30)


# kline
def kline_handle():
    while True:
        is_restart = False
        for item in item_list:
            cur_timestamp = int(time.time())
            db_timestamp_kline = query_kline(item[0], item[1])
            logger.info('item is: %s, current timestamp:%s (%s) , db timestamp:%s (%s), ' %
                            (str(item[0])+'_'+str(item[1]+'_'+item[2]), cur_timestamp, format_time(cur_timestamp),
                            db_timestamp_kline, format_time(db_timestamp_kline)))
            if cur_timestamp - db_timestamp_kline > 120:
                restart(item[2] + '_kline')
                logger.info('begin sleep 300s after restart %s_kline' % item[2])
                time.sleep(300)
                logger.info('finish sleep 300s after restart %s_kline' % item[2])
                is_restart = True
        if not is_restart:
            logger.info('all kline is normal, sleep 60s before next query')
            time.sleep(60)


# trade
def trade_handle():
    while True:
        is_restart = False
        for item in item_list:
            cur_timestamp_2 = int(time.time())
            db_timestamp_trade = query_trade(item[0], item[1])
            logger.info('item is: %s, current timestamp:%s (%s) , db timestamp:%s (%s), ' %
                            (str(item[0])+'_'+str(item[1]+'_'+item[2]), cur_timestamp_2, format_time(cur_timestamp_2),
                                db_timestamp_trade, format_time(db_timestamp_trade)))
            if cur_timestamp_2 - db_timestamp_trade > 120:
                restart(item[2] + '_trade')
                logger.info('begin sleep 120s after restart %s_trade' % item[2])
                time.sleep(120)
                is_restart = True
                logger.info('finish sleep 120s after restart %s_trade' % item[2])
        if not is_restart:
            logger.info('all trade is normal, sleep 30s before next query')
            time.sleep(30)


# depth
def depth_handle():
    dict1 = dict()
    # 保存每个交易所每个交易对的上次查询结果，结果为字典
    result_dict = {}
    for item in item_list:
        result_dict[item[1]+'_'+item[2]] = ''

    while True:
        is_restart = False
        for item in item_list:
            symbol_rst = dict(query_depth(item[0], item[1]))
            logger.info('item is: %s,last result is: %s, current result is: %s' %
                        (str(item[0])+'_'+str(item[1])+'_'+str(item[2]), str(result_dict[item[1]+'_'+item[2]]),
                         str(symbol_rst)))
            if cmp(result_dict[item[1]+'_'+item[2]], symbol_rst) == 0:
                    restart(item[2] + '_depth')
                    logger.info('begin sleep 120s after restart %s_depth' % item[2])
                    time.sleep(120)
                    is_restart = True
                    logger.info('finish sleep 120s after restart %s_depth' % item[2])
            result_dict[item[1] + '_' + item[2]] = symbol_rst.copy()

        if not is_restart:
            logger.info('all depth is normal, sleep 30s before next query')
            time.sleep(30)


if __name__ == '__main__':
    cur0 = get_mysqlcur()
    sql = "SELECT	t1.`exchange_id`,t1.`symbol`,t2.`name` as exchange_name FROM `symbols` t1" \
        " JOIN `exchanges` t2 ON t1.`exchange_id` =t2.`id` WHERE (t1.`base_currency` ='BTC' AND" \
        " (t1.`quote_currency`='USD' OR t1.`quote_currency`='USDT'))OR (t1.`base_currency`='ETH' AND " \
        "t1.`quote_currency`='BTC')"
    cur0.execute(sql)
    item_list = cur0.fetchall()
    cur0.close()
    # 目前所有交易对
    # ((1, 'btcusdt', 'huobipro'), (1, 'ethbtc', 'huobipro'), (2, 'tBTCUSD', 'bitfinex'),
    # (2, 'tETHBTC', 'bitfinex'), (3, 'BTCUSDT', 'binance'), (3, 'ETHBTC', 'binance'))

    ticket_thread = Thread(target=ticker_handle, name='ticker_thread')
    kline_thread = Thread(target=kline_handle, name='kline_thread')
    trade_thread = Thread(target=trade_handle, name='trade_thread')
    depth_thread = Thread(target=depth_handle, name='depth_thread')

    ticket_thread.start()
    kline_thread.start()
    trade_thread.start()
    depth_thread.start()

    logger.info('start monitor daemon')