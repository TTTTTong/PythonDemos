import random
from threading import Thread

import time


def func1(i):
    print('begin run:', i)
    time.sleep(random.randrange(5))
    print('end:', i)


t1 = Thread(target=func1, args=(1,))
t2 = Thread(target=func1, args=(3,))
t3 = Thread(target=func1, args=(2,))

t1.start()
t2.start()
t3.start()

t1.join()