import re
import webbrowser
import requests
import json


class Taobao:
    def __init__(self):
        self.loginURL = 'https://login.taobao.com/member/request_nick_check.do'
        self.loginHeaders = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Connection': 'keep-alive',
            'Content-Length': '3046',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'login.taobao.com',
            'Referer': 'https://login.taobao.com/member/login.jhtml?redirectURL=https%3A%2F%2Fwww.taobao.com%2F',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0'
        }
        self.username = '15529208705'
        self.ua = '106#+YoBgQBLBuDBGQKaBBBBBpZb54rZS0Gi94iYL0pc74/uSCZY5udZt0py7VrYD0Yb549uy0ds5V/Vpb5i5fsZTiGY7Vbf0JkKBBgbylZwsMtlw6SKBB8byltdmW2/BCBEylmi4gO0ylmbyl333p0bkImbyzzz0qphylmRggO0S6lbyl333pWbEzLKBlYh6Dm51E2XtQDc7hcUPZpzAm9s2qAepuO93Uy/SdbeqOZYkNcUPZpzAm9a63a4AjDo9fCxH2L09fGYm4uhQQ+UKfKUd8uSDhpmtC5Tr+ToBQphGhHajYTHpuOM2cAtDhpmtC9EFxzAdDYg7URYTO1YWXbOncUdAet0vjiIyJ97vZGO7URYTOTSBjba63a4AjDpdfi1cyi4+ZLutPXINpOICudzv8avZV+97hJua5y0tZtQtXqPag/5lYLNqvapKjB57mZ1FxQm5TBj+feuOZGbBTtfm6lnBP9AdW0UaJQuoLZYtQ8HjDGYkotuGHmopuQD…KTRylDv34r6KCCmaNJ5+SRGUzUZCCLTfkRkNCoBAVlb1Zzz5ZSpKB3a7TLNRkung+pKXf02RkU5BCB5tcmi4gOLgBDoBFxMWf7kRtMkLDo++DgkR+LKBKTRylDv3AeaKCCmaNJ5+SRGUzUZCCLTfkRkNCoBAVlb1Zzz5bLpKB3a7TLNRkung+pKXf02RkU5BCB5tcmi4gOP9BDoBFxMWf7kRtMkLDo++DgkR+LKBKTRylDv3A9XKCCmaNJ5+SRGUzUZCCLTfkRkrboBKlBb1ZziBCBVtcpG4J/0ymhlQaxGeednfQuoQV1klkQiBCBVtcpo4JK0ymu8QaxGeednfQuoQV1klkQiBCBVtcpq4zY0ymhPQaxGeednfQuoQV1klkQiBCBVtcpd4zK0ymhIQaxGeednfQuoQV1klkQiBCBVtcpf4zp0y4iuQaxGeednfQuoQV1klkQJBCB8tcpf4zp0ylmbq0DvtQroe9OnPAxr2DQGfSQ1BCBoBBKM7Q=='
        self.TPL_password_2 = '414efe534360e0ed2b60fd340bc867235b4b20046cd52afb86bca5050fb282ec2f8f371f63614912cb50fed1d72b4d9d83f48e104fd234926c700efde029f8890360f03a47c4fc4e3381e0602af0410d52012f55c3920a8802b686a1be065e604364f0df68a2a2c3a6eb0cf98a12637300de4030834519e7a8d118adaade5a3c'
        self.post = {
            'ua': self.ua,
            'TPL_checkcode': '',
            'CtrlVersion': '1,0,0,7',
            'TPL_password': '',
            'TPL_redirect_url': 'http://i.taobao.com/my_taobao.htm?nekot=udm8087E1424147022443',
            'TPL_username': self.username,
            'loginsite': '0',
            'newlogin': '0',
            'from': 'tb',
            'fc': 'default',
            'style': 'default',
            'css_style': '',
            'tid': 'XOR_1_000000000000000000000000000000_625C4720470A0A050976770A',
            'support': '000001',
            'loginType': '4',
            'minititle': '',
            'minipara': '',
            'umto': 'NaN',
            'pstrong': '3',
            'llnick': '',
            'sign': '',
            'need_sign': '',
            'isIgnore': '',
            'full_redirect': '',
            'popid': '',
            'callback': '',
            'guf': '',
            'not_duplite_str': '',
            'need_user_id': '',
            'poy': '',
            'gvfdcname': '10',
            'gvfdcre': '',
            'from_encoding ': '',
            'sub': '',
            'TPL_password_2': self.TPL_password_2,
            'loginASR': '1',
            'loginASRSuc': '1',
            'allp': '',
            'oslanguage': 'zh-CN',
            'sr': '1366*768',
            'osVer': 'windows|6.1',
            'naviVer': 'firefox|35'
        }

    # 判断是否需要验证码
    def ifNeedIdenCode(self):
        response = requests.post(url=self.loginURL, data=json.dumps(self.post), headers=self.loginHeaders)
        content = response.text
        print(content)

        if response.status_code == 200:
            print(u'获取请求成功！')
            # \u8bf7\u8f93\u5165\u9a8c\u8bc1\u7801 这六个字是请输入验证码的utf-8编码
            pattern = re.compile('\u8bf7\u8f93\u5165\u9a8c\u8bc1\u7801', re.S)
            result = re.search(pattern, content)

            if result:
                print(u'此次登陆需要输入验证码')
                return content
            else:
                print(u'此次请求不需要输入验证码')
                return False
        else:
            print(u'获取请求失败')

    # 获取验证码图片
    def getIdenCode(self, page):
        pattern = re.compile('<img id="J_StandardCode_m.*?data-src="(.*?)"', re.S)
        result = re.search(pattern, page)

        # 匹配到内容且验证码链接不为空
        if result and result.group(1):
            print(result.group(1))
            return result.group(1)
        else:
            print(u'没有获取到验证码')
            return False

    def main(self):
        # 判断是否需要验证码
        isNeed = self.ifNeedIdenCode()
        if isNeed:
            print(u'需要手动输入验证码')
            idencode = self.getIdenCode(isNeed)

            if idencode:
                print(u'获取验证码成功，请在浏览器中输入你看到的验证码')
                webbrowser.open_new_tab(isNeed)
            else:
                print(u'获取验证码失败')


if __name__ == '__main__':
    tb = Taobao()
    tb.main()
