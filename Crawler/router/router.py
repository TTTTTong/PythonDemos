import http.cookiejar
import json
from urllib.parse import urlencode
import urllib.request


class Router:
    def __init__(self):
        self.loginURL = 'http://192.168.1.1/'
        self.cookie = http.cookiejar.LWPCookieJar()
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0',
            'Content-Type': 'application/json; charset=UTF-8',
        }
        self.postdata = urlencode({
            'method': 'do',
            'login': {'password': self.encrypt_pwd('7573066')}
        }).encode()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookie))

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
        request = urllib.request.Request(url=self.loginURL, data=self.postdata, headers=self.header)
        response = self.opener.open(request)
        stok = json.loads(response.txt)['stok']

        return stok

    def getList(self, stok):
        getURL = '%sstok=%s/ds' % stok
        postdata = '{hosts_info: {table: "online_host"}, method: "get"}'
        request = urllib.request.Request(url=getURL, data=postdata, headers=self.header)
        respone = self.opener.open(request)

        print(respone.read().decode())


if __name__ == '__main__':
    new = Router()
    new.getList(new.getStok())