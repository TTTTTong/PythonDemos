from pprint import pprint

from PIL import Image


im = Image.open('identify code.jpg')
# 将图片转换为8位像素模式(大写P)
im.convert('P')

# 颜色直方图
his = im.histogram()

values = {}
for i in range(256):
    values[i] = his[i]

