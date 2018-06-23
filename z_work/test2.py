import MySQLdb
import logging

logging.basicConfig(level=logging.INFO, filename='monitor_info.log', format=' %(asctime)s - %(levelname)s - %(message)s')
logging.basicConfig(level=logging.ERROR, filename='monitor_error.log', format=' %(asctime)s - %(levelname)s - %(message)s')
logging.info('start monitor daemon')
conn = MySQLdb.connect(host='rm-j6ccb77fan1q3p0n8.mysql.rds.aliyuncs.com',
                           user='rshvip', passwd='Aa112255', db='coindata')
cur = conn.cursor()
sql3 = "SELECT	t1.`exchange_id`,t1.`symbol`,t2.`name` as exchange_name FROM `symbols` t1 JOIN `exchanges` t2 ON t1.`exchange_id` =t2.`id`  WHERE (t1.`base_currency` ='BTC' AND (t1.`quote_currency`='USD' OR t1.`quote_currency`='USDT')) OR (t1.`base_currency`='ETH' AND t1.`quote_currency`='BTC')"
sql0 = "SELECT `close` FROM  `market_ticker` WHERE `exchange_id` =1 AND `symbol` ='btcusdt'"
sql = "SELECT `time` FROM `market_history_trade` WHERE `exchange_id`=1 AND `symbol`='btcusdt' ORDER BY `time` DESC LIMIT 1"
sql4 = "SELECT `time` FROM `market_kline` WHERE `exchange_id`=1 AND `symbol`='btcusdt' AND `period`=1 ORDER BY `time` DESC LIMIT 1"
sql5 = "SELECT t1.`quote_currency`,t1.`base_currency`,GROUP_CONCAT(t1.`exchange_id` order by t4.`priority`) as exchange_ids,GROUP_CONCAT(t1.`symbol`) as symbols,t2.`priority` as base_priority,t3.`priority` as quote_priority FROM `symbols` t1 JOIN `currency_info` t2 ON t1.base_currency=t2.currency JOIN `currency_info` t3 ON t1.quote_currency=t3.currency JOIN `exchanges` t4 ON t1.`exchange_id` =t4.`id` WHERE t1.base_currency LIKE '%ETH%' GROUP BY t1.quote_currency,t1.base_currency ORDER BY `base_priority`,`quote_priority`"
cur.execute(sql5)
print (cur.fetchall())
