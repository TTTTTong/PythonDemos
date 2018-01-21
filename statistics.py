import sys
import os


def count():
    code = 0
    comment = 0
    blank = 0
    in_multi_comment = False

    for dirpath, dirnames, filenames in os.walk(sys.path[0]):
        for filename in filenames:
            file = os.path.join(dirpath, filename)

            if file.endswith('.py'):
                with open(file, encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()

                        if line == '' and not in_multi_comment:
                            blank += 1

                        # 注释共有四种：
                        # 1. '#'开头的单行注释
                        # 2. '"""'或"'''"开头且结尾的单行注释
                        # 3. 多行注释之间的行
                        elif line.startswith("#") or \
                                (line.startswith('"""') and line.endswith('"""')) > 2 or \
                                (line.startswith("'''") and line.endswith("'''")) > 2 or \
                                (in_multi_comment and not (line.startswith('"""') or line.startswith("'''"))):
                            comment += 1
                        # 4. '"""'或者"'''"开头或者结尾的单行注释()
                        elif line.startswith('"""') or line.startswith("'''"):
                            comment += 1
                            # 开始或结束多行注释
                            in_multi_comment = not in_multi_comment
                        else:
                            code += 1

    print('code: '.ljust(10, ' '), code)
    print('comment: '.ljust(10, ' '), comment)
    print('blank:'.ljust(10, ' '), blank)


if __name__ == '__main__':
    count()
