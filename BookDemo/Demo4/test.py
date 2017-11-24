from nntplib import *
from time import *
import datetime
day = 24*60*60
ystd = localtime(time() - day)

# date = strftime('%y%m%d', ystd)
date= datetime.date(2017, 9, 24)
hour = strftime('%H%M%S', ystd)
servername = ('web.aioe.org')
group = 'comp.lang.python.announce'

server = NNTP(servername)

ids = server.newnews(group, date)[1]
print(ids)
for id in ids:
    head = server.head(id)[1]
    print(head)
    # head = server.article(id)[3]
    for line in head:
        if str(line).lower().startswith('subject:'):
            subject = line[9:]
            break
    body = server.body(id)[3]
    print(server.body(id))
    print(subject)
    print('-'*len(subject))
    print('\n'.join(body))
server.quit()