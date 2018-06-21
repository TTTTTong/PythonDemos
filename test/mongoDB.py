import time

def format_time(timestamp):
    return time.strftime('%H:%M:%S', time.localtime(timestamp))

print (format_time(1529547060))