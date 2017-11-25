import argparse
from PIL import Image

'''
将图片转化为字符串
'''

# 解析命令行参数设置

# parser = argparse.ArgumentParser()
#
# parser.add_argument('file')
# parser.add_argument('-o', '--output')
# parser.add_argument('--width', type=int, default=80)
# parser.add_argument('--height', type=int, default=80)
#
# args = parser.parse_args()
#
# IMG = args.file

WIDTH = 80
HEIGHT = 80
OUTPUT = 'result.txt'
# ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")
ascii_char = list("........................................................................ ")


# 将256个灰度映射到70个字符上
def get_char(r, g, b, alpha=256):
    if alpha == 0:
        return ' '
    length = len(ascii_char)
    gray = int(0.2126*r + 0.7152*g + 0.0722*b)
    unit = (256.0 + 1)/length
    # gary/(256+1)*length = gray*(length/(256+1)) = gray/unit
    return ascii_char[int(gray/unit)]


def writeToTxt(txt):
    with open(OUTPUT, 'w') as f:
        f.write(txt)


def main():
    im = Image.open('ascii_dora.png')
    im = im.resize((WIDTH, HEIGHT), Image.NEAREST)

    txt = ""

    for i in range(HEIGHT):
        for j in range(WIDTH):
            txt += get_char(*im.getpixel((j, i)))
        txt += '\n'

    writeToTxt(txt)


if __name__ == '__main__':
    main()
