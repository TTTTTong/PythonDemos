import random
from multiprocessing import Pool
import os
import time


def func1(i):
    print('begin run %s [%s]' % (i, os.getpid()))
    time.sleep(random.randrange(4))
    print('end run %s [%s]' % (i, os.getpid()))


if __name__ == '__main__':
    p = Pool(4)
    # for i in range(7):
    #     p.apply_async(func1, (i, ))
    # p.close()  # 调用之后就不能添加新的process
    # p.join()
    # print('done')

    result = p.map_async(func1, range(7))
    # print(result)
    print('===')

    # result = [p.apply_async(func1, (i, )) for i in range(7)]
    # print([res.get() for res in result])