from urllib import request
from reportlab.graphics.shapes import *
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics import renderPDF

URL = 'http://services.swpc.noaa.gov/text/predicted-sunspot-radio-flux.txt'
COMMENT = '#:'

drawing = Drawing(400, 200)
data = []
for line in request.urlopen(URL).readlines():
    # print('123')
    # print(line)
    # print(type(line))
    # print(line[0])
    if not line.decode().isspace() and not line.decode()[0] in COMMENT:
        data.append([n for n in line.decode().split()])

pred = [float(row[2]) for row in data]
high = [float(row[3]) for row in data]
low  = [float(row[4]) for row in data]
time = [float(int(row[0])+int(row[1])/12.0) for row in data]

lp = LinePlot()
lp.x = 50
lp.y = 50
lp.height = 125
lp.width = 300
print(list(zip(time, pred)))
lp.data = [list(zip(time, pred)), list(zip(time, high)), list(zip(time, low))]
lp.lines[0].strokeColor = colors.blue
lp.lines[1].strokeColor = colors.red
lp.lines[2].strokeColor = colors.green

drawing.add(lp)
drawing.add(String(250, 150, 'sunspots', fontsize=14, fillColor=colors.red))

renderPDF.drawToFile(drawing, 'report3.pdf','Sunspots')
