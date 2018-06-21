from multiprocessing.dummy import Pool as ThreadPool
import time
import threading
import multiprocessing


print (multiprocessing.cpu_count())


def fun1(i):
    print('start:', i, threading.current_thread().getName())
    time.sleep(2)
    print('end:', i)
    return i

# map_async
# pool = ThreadPool(3)
# result = pool.map_async(fun1, range(5))
# result.wait()
# print(']]', result.ready())
# print(']]', result.successful())
# print('[]', result.get())
# print('===')


# map
# mappool = ThreadPool(3)
# result = mappool.map(fun1, range(5))
# mappool.close()
# mappool.join()
# print('====')


# apply_async
asyncpool = ThreadPool(3)
re_list = []
for i in range(5):
    result = asyncpool.apply_async(fun1, (i,))
    time.sleep(0.1)
    re_list.append(result)
asyncpool.close()
asyncpool.join()
for i in re_list:
    i.wait()
for i in re_list:
    if i.ready():
        if i.successful():
            print(i.get())
print('===')


# apply
# apply_pool = ThreadPool(3)
# re_list = []
# for i in range(5):
#     result = apply_pool.apply(fun1, (i,))
#     re_list.append(result)
# print(re_list)
