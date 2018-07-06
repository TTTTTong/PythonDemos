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


def get_mysqlcur():
    pass


# 从数据库获取各项最新值
def query_ticker(exchange_id):
    cur_ticker = get_mysqlcur()
    sql = "SELECT `time` FROM `market_ticker` WHERE `exchange_id` =%s ORDER BY `time` DESC LIMIT 1"
    cur_ticker.execute(sql, args=(exchange_id,))
    res = cur_ticker.fetchone()
    if res is None:
        logger.info('query_ticker is None, return 0, exchanged_id is:%s' % exchange_id)
        res = 0
    else:
        res = res[0]
    cur_ticker.close()
    return res


def query_kline(excahnge_id):
    cur_kline = get_mysqlcur()
    sql = "SELECT  `time` from `market_kline`  WHERE `exchange_id` =%s AND `period` =1 ORDER BY `time` DESC LIMIT 1 "
    cur_kline.execute(sql, args=(excahnge_id,))
    res = cur_kline.fetchone()
    if res is None:
        logger.info('query_kline is None, return 0, exchanged_id is:%s' % excahnge_id)
        res = 0
    else:
        res = res[0]
    cur_kline.close()
    return res


def query_trade(exchange_id):
    cur_trade = get_mysqlcur()
    sql = "SELECT `time` FROM `market_history_trade` WHERE `exchange_id`=%s ORDER BY `time` DESC LIMIT 1"
    cur_trade.execute(sql, args=(exchange_id,))
    res = cur_trade.fetchone()
    if res is None:
        logger.info('query_trade is None, return 0, exchanged_id is:%s' % exchange_id)
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


# 时间戳转换为(时:分:秒)格式
def format_time(timestamp):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))


# 各项的处理函数, 决定是否重启对应服务
# ticket
def ticker_handle(exchange_id, exchange):
    while True:
        is_restart = False
        cur_timestamp = int(time.time())
        db_timestamp = query_ticker(exchange_id)
        logger.info('item is: %s, current timestamp:%s (%s) , db timestamp:%s (%s), ' %
                        (exchange+'_ticker', cur_timestamp, format_time(cur_timestamp),
                            db_timestamp, format_time(db_timestamp)))
        if cur_timestamp - db_timestamp > 300:
            restart(exchange + '_ticker')
            logger.info('begin sleep 120s after restart %s_ticker' % exchange)
            time.sleep(120)
            is_restart = True
            # logger.info('finish sleep 120s after restart %s_trade' % item[2])
        if not is_restart:
            logger.info('all ticker is normal, sleep 30s before next query')
            time.sleep(30)


# kline
def kline_handle(exchange_id, exchange):
    while True:
        is_restart = False
        cur_timestamp = int(time.time())
        db_timestamp = query_kline(exchange_id)
        logger.info('item is: %s, current timestamp:%s (%s) , db timestamp:%s (%s), ' %
                        (exchange+'_kline', cur_timestamp, format_time(cur_timestamp),
                        db_timestamp, format_time(db_timestamp)))
        if cur_timestamp - db_timestamp > 300:
            restart(exchange + '_kline')
            logger.info('begin sleep 300s after restart %s_kline' % exchange)
            time.sleep(300)
            # logger.info('finish sleep 300s after restart %s_kline' % item[2])
            is_restart = True
        if not is_restart:
            logger.info('all kline is normal, sleep 60s before next query')
            time.sleep(60)


# trade
def trade_handle(exchange_id, exchange):
    while True:
        is_restart = False
        cur_timestamp = int(time.time())
        db_timestamp = query_trade(exchange_id)
        logger.info('item is: %s, current timestamp:%s (%s) , db timestamp:%s (%s), ' %
                        (exchange+'_trade', cur_timestamp, format_time(cur_timestamp),
                            db_timestamp, format_time(db_timestamp)))
        if cur_timestamp - db_timestamp > 300:
            restart(exchange + '_trade')
            logger.info('begin sleep 120s after restart %s_trade' % exchange)
            time.sleep(120)
            is_restart = True
            # logger.info('finish sleep 120s after restart %s_trade' % item[2])
        if not is_restart:
            logger.info('all trade is normal, sleep 30s before next query')
            time.sleep(30)


# depth
def depth_handle(exchange_id, exchange, symbol):
    # 保存交易所每个交易对的上次查询结果，字典形式
    result_dict = dict()
    result_dict[str(exchange_id)+'_'+symbol] = ''

    while True:
        is_restart = False
        symbol_rst = dict(query_depth(exchange_id, symbol))
        logger.info('item is: %s,last result is: %s, current result is: %s' %
                    (str(exchange_id)+':'+symbol+':'+exchange, str(result_dict[str(exchange_id)+'_'+symbol]),
                     str(symbol_rst)))
        #  3.x没有cmp函数
        if cmp(result_dict[str(exchange_id)+'_'+symbol], symbol_rst) == 0:
                restart(exchange + '_depth')
                logger.info('begin sleep 120s after restart %s_depth' % exchange)
                time.sleep(120)
                is_restart = True
                # logger.info('finish sleep 120s after restart %s_depth' % item[2])
        result_dict[str(exchange_id)+'_'+symbol] = symbol_rst.copy()

        if not is_restart:
            logger.info('all depth is normal, sleep 300s before next query')
            time.sleep(300)


if __name__ == '__main__':
    cur0 = get_mysqlcur()
    sql = "SELECT `id` ,`name`   FROM `exchanges` "
    cur0.execute(sql)
    # 所有的交易所列表(id, 英文名称)
    exchange_list = cur0.fetchall()
    cur0.close()

    # depth特殊处理,因为部分交易所不支持btc,先查出支持btc的交易所
    depth_cur = get_mysqlcur()
    depth_sql = "SELECT	t1.`exchange_id`,t1.`symbol`,t2.`name_zh`  as exchange_name FROM `symbols` t1" \
                " JOIN `exchanges` t2 on t1.`exchange_id` =t2.`id` WHERE t1.`base_currency` ='btc' " \
                " GROUP BY `id` "
    depth_cur.execute(depth_sql)
    exchange_supBTC_list = depth_cur.fetchall()
    depth_cur.close()
    # key:exchange_id, value:exchange_id,symbol,name_zh
    exchange_sup_btc = {}
    for item in exchange_supBTC_list:
        exchange_sup_btc[item[0]] = item

    logger.info('start monitor daemon')
    # 给每个交易所的每个接口开启一个线程,共有交易所数*4个线程
    for item in exchange_list:
        ticket_thread = Thread(target=ticker_handle, name=item[1] + '_ticker_thread', args=(item[0], item[1]))
        kline_thread = Thread(target=kline_handle, name=item[1] + '_kline_thread', args=(item[0], item[1]))
        trade_thread = Thread(target=trade_handle, name=item[1] + '_trade_thread', args=(item[0], item[1]))
        # 当前交易所支持btc
        if exchange_sup_btc.has_key(item[0]):  # (3.x将 has_key 替换为 in)
            depth_thread = Thread(target=depth_handle, name=item[1]+'_depth_thread', args=(exchange_sup_btc[item[0]][0],
                                                                                           item[1],
                                                                                           exchange_sup_btc[item[0]][1]))
        # 交易所不支持btc,选出此交易所最近交易中成交额最高的一个交易对
        else:
            sql_temp = "SELECT `exchange_id` ,`symbol` ,SUM(`usd_vol`) usd_vol FROm `market_history_trade`" \
                       " WHERE `exchange_id` =%s  GROUP BY `symbol` ORDER BY usd_vol DESC LIMIT 1;"
            cur_temp = get_mysqlcur()
            cur_temp.execute(sql_temp, args=(item[0],))
            res = cur_temp.fetchone()
            cur_temp.close()
            depth_thread = Thread(target=depth_handle, name=item[1] + '_depth_thread', args=(res[0], item[1], res[1]))

        ticket_thread.start()
        kline_thread.start()
        trade_thread.start()
        depth_thread.start()
