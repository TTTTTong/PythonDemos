import http.cookiejar
import requests
import json


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
        self.cookie = http.cookiejar.CookieJar()
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0',
            'Content-Type': 'application/json; charset=UTF-8',
        }
        # 这样直接写麻烦的话可以先写成字典再用json.dumps()转换
        self.postdata = '{"method": "do", "login": {"password": "%s"}}' % self.encrypt_pwd('7573066')

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

        return stok

    def getList(self, stok):
        getURL = '%sstok=%s/ds' % (self.loginURL, stok)
        postdata = '{"hosts_info": {"table": "online_host"}, "method": "get"}'
        response = requests.post(url=getURL, data=postdata, headers=self.header)

        print(response.text)
        # for l in json.loads(response.text)['hosts_info']['online_host']:
        #     for k, v in l.items():
        #         for k2, v2 in v.items():
        #             if k2 == 'hostname':
        #                 username = urllib.parse.unquote(v2)
        #             elif k2 == 'ip':
        #                 ip = v2
        #             elif k2 == 'up_speed':
        #                 upspeed = v2
        #             elif k2 == 'down_speed':
        #                 downspeed = v2
        #         print('用户名：' + username, 'IP地址：' + ip, '上传速度：' + upspeed + 'B/s', '下载速度：' + downspeed + 'B/s')


if __name__ == '__main__':
    new = Router()
    new.getList(new.getStok())
