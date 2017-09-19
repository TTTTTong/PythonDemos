import re
import sys

from Demo1.utils import *

print ('<html><head><title>...</title><body>')

title = True
for block in blocks(sys.stdin):
    block = re.sub(r'\*(.+?)\*',r'<em>\</em>',block)
    if title:
        print ('<h1>')
        print (block)
        print ('</h1>')
        title = False
    else:
        print ('<p>')
        print (block)
        print ('</p>')

print ('</body></html>')
