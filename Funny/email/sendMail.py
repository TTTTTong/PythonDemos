# -*- coding: utf-8 -*-
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email import encoders
from email.utils import parseaddr, formataddr
import smtplib


def _format_addr(s):
    name, addr = parseaddr(s)
    # print('name:'+name+'  addr:'+addr)
    # print(formataddr((Header(name, 'utf-8').encode(), addr))+'0.0')
    return formataddr((Header(name, 'utf-8').encode(), addr))


from_addr = input('From:')
password = input('Password:')
to_addr = input('To:')
smtp_server = input('SMTP_server:')

msg = MIMEMultipart()
msg['From'] = _format_addr('python<%s>' % from_addr)
msg['To'] = _format_addr('manager<%s>' % to_addr)
msg['Subject'] = Header('greeting from smtp', 'utf-8').encode()
# 添加正文
msg.attach(MIMEText('send with fil...', 'plain', 'utf-8'))
# 添加附件就是加上一个MIMEBase，从本地读取图片
with open(r'D:\Picture\picture、\123.png', 'rb') as f:
    # 设置附件的MIME和文件名
    mime = MIMEBase('image', 'png', filename='123.png')
    # 必要的头信息
    mime.add_header('Content-Disposition', 'attachment', filename='123.png')
    mime.add_header('Content-ID', '<0>')
    mime.add_header('X-Attachment-Id', '0')
    # 读入附件内容
    mime.set_payload(f.read())
    # 用Base64编码
    encoders.encode_base64(mime)
    # 添加到MIMEMultipart
    msg.attach(mime)

server = smtplib.SMTP(smtp_server, 25)
server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()

