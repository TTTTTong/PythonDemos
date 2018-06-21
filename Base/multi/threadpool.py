import random
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import time, os

# ProcessPoolExecutor用法相同


def test_fun(i):
    print('start:', i)
    time.sleep(random.randrange(4))
    print('end:', i)
    return i


executor = ThreadPoolExecutor(3)
# result_ite = executor.map(test_fun, range(6))
# print([i for i in result_ite])

result = executor.submit(test_fun, '1')
result2 = executor.submit(test_fun, '2')

print('sleeping')
print(result.done())
print(result.cancel())
print(result.result())
time.sleep(4)
result3 = executor.submit(test_fun, '5')
