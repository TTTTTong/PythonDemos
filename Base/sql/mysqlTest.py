import pymysql


conn = pymysql.connect(host='localhost', port=3306, user='root', password='201919', database='test')

cur = conn.cursor()
# result = cur.execute('select * from alchemyTest')
result = cur.executemany('insert into alchemyTest2(noname) values(%s)', [('first',), ('second',)])

cur.close()
conn.commit()
conn.close()

print(result)