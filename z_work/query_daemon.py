import MySQLdb
import commands
import redis
import time
import logging
import logging.config
import os

logging.config.fileConfig(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'log.conf'))
logger = logging.getLogger('monitor')
logger.info('start monitor daemon')
# logging.basicConfig(level=logging.INFO, filename='monitor_info.log', format=' %(asctime)s - %(levelname)s - %(message)s')
# logging.info('start monitor daemon')


def get_mysqlcur():
    conn = MySQLdb.connect(host='rm-j6ccb77fan1q3p0n8.mysql.rds.aliyuncs.com',
                           user='rshvip', passwd='Aa112255', db='coindata')
    cur = conn.cursor()
    return cur


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


def restart(name):
    command = 'pm2 restart ' + name
    commands.getstatusoutput(command)
    logger.error('restart:%s' % name)


def format_time(timestamp):
    return time.strftime('%H:%M:%S', time.localtime(timestamp))


cur0 = get_mysqlcur()
sql = "SELECT	t1.`exchange_id`,t1.`symbol`,t2.`name` as exchange_name FROM `symbols` t1" \
      " JOIN `exchanges` t2 ON t1.`exchange_id` =t2.`id` WHERE (t1.`base_currency` ='BTC' AND" \
      " (t1.`quote_currency`='USD' OR t1.`quote_currency`='USDT'))OR (t1.`base_currency`='ETH' AND " \
      "t1.`quote_currency`='BTC')"
cur0.execute(sql)
result = cur0.fetchall()
cur0.close()


for item in result:

    # for ticket
    temp1, temp2, temp3 = 1, 2, 3
    # for depth
    dict1 = dict()

    while True:
        is_restart = False
        # ticket
        temp1, temp2 = temp2, temp3
        temp3 = query_ticker(item[0], item[1])
        if temp1 == temp2 == temp3:
            logger.info('item is:%s,last three result: %s, %s, %s' % (str(item[0])+'_'+str(item[1]+'_'+item[2]), temp1, temp2,
                                                                       temp3))
            restart(item[2] + '_ticker')
            is_restart = True
            time.sleep(120)
            logger.info('sleep 120s after restart %s_ticket' % item[2])

        # kline
        cur_timestamp = int(time.time())
        db_timestamp_kline = query_kline(item[0], item[1])
        if cur_timestamp - db_timestamp_kline > 120:
            logger.info('item is:%s, current timestamp:%s (%s) , db timestamp:%s (%s), ' %
                        (str(item[0])+'_'+str(item[1]+'_'+item[2]), cur_timestamp, format_time(cur_timestamp),
                         db_timestamp_kline, format_time(db_timestamp_kline)))
            restart(item[2] + '_kline')
            is_restart = True
            time.sleep(120)
            logger.info('sleep 120s after restart %s_kline' % item[2])

        # trade
        cur_timestamp_2 = int(time.time())
        db_timestamp_trade = query_trade(item[0], item[1])
        if cur_timestamp_2 - db_timestamp_trade > 120:
            logger.info('item is:%s, current timestamp:%s (%s) , db timestamp:%s (%s), ' %
                        (str(item[0])+'_'+str(item[1]+'_'+item[2]), cur_timestamp_2, format_time(cur_timestamp_2),
                         db_timestamp_trade, format_time(db_timestamp_trade)))
            restart(item[2] + '_trade')
            is_restart = True
            time.sleep(120)
            logger.info('sleep 120s after restart %s_trade' % item[2])

        # depth
        dict2 = dict(query_depth(item[0], item[1]))
        if cmp(dict1, dict2) == 0:
                restart(item[2] + '_depth')
                is_restart = True
                time.sleep(120)
                logger.info('sleep 120s after restart %s_depth' % item[2])
        dict1 = dict2.copy()
        
        if not is_restart:
            logger.info('all is normal, sleep 30s before next query')
            time.sleep(30)
