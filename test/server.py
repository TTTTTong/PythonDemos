import sys
import os
# print(os.walk(sys.path))
for i, j, k in os.walk(sys.path[0]):
    print(i, j, k)