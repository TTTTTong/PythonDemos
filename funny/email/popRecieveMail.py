import poplib
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr

email = input('Email:')
password = input('Password:')
pop3_server = input('Pop3_Server:')

server = poplib.POP3(pop3_server)
server.set_debuglevel(1)
print(server.getwelcome().decode())

# 身份认证
server.user(email)
server.pass_(password)
# stat()返回email数量和占用空间
print('Message:%s Size: %s' % server.stat())
# list()返回所有email编号
resp, mails, octets = server.list()
# print(mails)
86
# 获取最新一封邮件(索引从1开始)
index = len(mails)
resp, lines, octets = server.retr(index)

# lines存储了Email的原始文本的每一行
msg_content = b'\r\n'.join(lines).decode()
msg = Parser().parsestr(msg_content)

# 可以根据email索引直接从服务器删除email
# server.dele(index)


def print_info(msg, indent=0):
    if indent == 0:
        for header in ['From', 'To', 'Subject']:
            value = msg.get(header, '')
            if value:
                if header == 'Subject':
                    value = decode_str(value)
                else:
                    hdr, addr = parseaddr(value)
                    name = decode_str(hdr)
                    value = u'%s <%s>' % (name, addr)
            print('%s%s:%s' % (' '*indent, header, value))
    if msg.is_multipart():
        parts = msg.get_payload()
        print('============')
        print(parts)
        print(enumerate(parts))
        print('=============')
        for n, part in enumerate(parts):
            print('%s part %s' % (''*indent, n))
            print('%s------------' % (''*indent))
            print_info(part, indent+1)

    else:
        content_type = msg.get_content_type()
        if content_type == 'type/plain' or content_type == 'text/html':
            content = msg.get_payload(decode=True)
            charset= guess_charset(msg)
            if charset:
                content = content.decode(charset)
            print('%s Text: %s' % (''*indent, content+'...'))
        else:
            print('%s Attachment: %s' % (''*indent, content_type))


def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value


def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos+8:].strip()
    return charset


print_info(msg)
server.quit()