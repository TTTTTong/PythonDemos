from nntplib import *
from time import strftime

date = strftime('%y%m%d')
hour = strftime('%H%M%S')
servername = ('web.aioe.org')
group = 'comp.lang.python.announce'

server = NNTP(servername)

ids = server.newnews(group, date)[1]
print(ids)