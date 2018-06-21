from random import randint
from PIL import Image, ImageFilter, ImageDraw, ImageFont


def rdmChar():
    return chr(randint(65, 90))


# 随机颜色1
def rdmColor():
    return randint(64, 255), randint(64, 255), randint(64, 255)


# 随机颜色2
def rdmColor2():
    return randint(32, 127), randint(32, 127), randint(32, 127)


width = 240
height = 60
image = Image.new('RGB', (width, height), (255, 255, 255))

# Font对象
font = ImageFont.truetype('C:\Windows\Fonts\Arial.ttf', 36)
draw = ImageDraw.Draw(image)
# 填充每个像素
for x in range(width):
    for y in range(height):
        draw.point((x, y), fill=rdmColor())

# 输出文字
for t in range(4):
    draw.text((60*t + 10, 10), rdmChar(), font=font, fill=rdmColor2())

# 模糊
# image = image.filter(ImageFilter.BLUR)
image.save('identify code.jpg')
image.show()