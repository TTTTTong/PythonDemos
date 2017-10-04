import socket
import threading
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 9999))
s.listen(5)
print('Waitting for connection...')

def tcplink(sock, addr):
    print('accept new connect from %s:%s' % addr)
    sock.send(b'welcome')
    while True:
        data = sock.recv(1024)
        time.sleep(1)
        if not data or data.decode() == 'exit':
            break
        sock.send(('hello, %s' % data.decode()).encode())
    sock.close()
    print('disconnection')


while True:
    sock, addr = s.accept()
    t = threading.Thread(target=tcplink, args=(sock, addr))
    t.start()
