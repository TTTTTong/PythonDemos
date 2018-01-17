import urllib
import requests
import json
import time
from writeToExcel import write


class Router:
    """
    模拟登陆路由器
    关键点：
    1.请求参数
    2.将js密码加密函数用python重写
    3.获取stok(获取之后才能进行获取数据等一系列操作)
    """
    def __init__(self):
        self.loginURL = 'http://192.168.1.1/'
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0',
            'Content-Type': 'application/json; charset=UTF-8',
        }
        # 这样直接嫌麻烦的话可以先写成字典再用json.dumps()转换
        # data = {'method': 'do', 'login': {'password': self.encrypt_pwd('7573066')}}
        # self.postdata = json.dumps(data)
        self.postdata = '{"method": "do", "login": {"password": "%s"}}' % self.encrypt_pwd('7573066')

        # 创建写入excel的对象
        self.writeObj = write()

    def encrypt_pwd(self, password):
        input1 = "RDpbLfCPsJZ7fiv"
        input3 = "yLwVl0zKqws7LgKPRQ84Mdt708T1qQ3Ha7xv3H7NyU84p21BriUWBU43odz3iP4rBL3cD02KZciXTysVXiV8ngg6vL48rPJ" \
                 "yAUw0HurW20xqxv9aYb4M9wK1Ae0wlro510qXeU07kV57fQMc8L6aLgMLwygtc0F10a0Dg70TOoouyFhdysuRMO51yY5ZlOZZLE" \
                 "al1h0t9YQW0Ko7oBwmCAHoic4HYbUyVeU3sfQ1xtXcPcf1aT303wAQhv66qzW"
        len1 = len(input1)
        len2 = len(password)
        dictionary = input3
        lenDict = len(dictionary)
        output = ''
        if len1 > len2:
            length = len1
        else:
            length = len2
        index = 0
        while index < length:
            # 十六进制数 0xBB 的十进制为 187
            cl = 187
            cr = 187
            if index >= len1:
                # ord() 函数返回字符的整数表示
                cr = ord(password[index])
            elif index >= len2:
                cl = ord(input1[index])
            else:
                cl = ord(input1[index])
                cr = ord(password[index])
            index += 1
            # chr() 函数返回整数对应的字符
            output = output + chr(ord(dictionary[cl ^ cr]) % lenDict)
        return output

    def getStok(self):
        response = requests.post(url=self.loginURL, data=self.postdata, headers=self.header)
        stok = json.loads(response.text)['stok']

        # print(response.text)
        return stok

    def getList(self, stok):
        getURL = '%sstok=%s/ds' % (self.loginURL, stok)
        postdata = '{"hosts_info": {"table": "online_host"}, "method": "get"}'
        response = requests.post(url=getURL, data=postdata, headers=self.header)

        # print(response.text)
        for l in json.loads(response.text)['hosts_info']['online_host']:
            for k, v in l.items():
                for k2, v2 in v.items():
                    if k2 == 'hostname':
                        username = urllib.parse.unquote(v2)
                    elif k2 == 'ip':
                        ip = v2
                    elif k2 == 'up_speed':
                        upspeed = v2
                    elif k2 == 'down_speed':
                        downspeed = v2
                    elif k2 == 'mac':
                        mac = v2

                result = [username, ip, mac, str(int(int(downspeed)/1024))+'KB/s', str(int(int(upspeed)/1024))+'KB/s']
                self.writeObj.writeAction(result)
                # print('用户名: {0:<17}, IP地址: {1}, MAC地址： {4}, 下载速度: {3:>5.0f}KB/s, 上传速度: {2:>3.0f}KB/s'
                # .format(username, ip, int(upspeed)/1024, int(downspeed)/1024, mac))


if __name__ == '__main__':
    new = Router()
    stok = new.getStok()
    while True:
        new.getList(stok)
        time.sleep(5)
        new.writeObj.writeAction(['-'*33]*3 + ['-'*18]*2)