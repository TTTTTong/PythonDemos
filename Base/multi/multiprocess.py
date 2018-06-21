import random
from multiprocessing import Process
import os

import time


def fun1(i):
    print('begin child process:', os.getpid(), i)
    time.sleep(random.randrange(4))
    print('endchild process:', os.getpid(), i)


p1 = Process(target=fun1, args=('1', ))
p2 = Process(target=fun1, args=('2', ))
p3 = Process(target=fun1, args=('3', ))

p1.start()
p2.start()
p3.start()

p1.join()
p2.join()
p3.join()

print('end')



