#!/usr/bin/python
#coding=utf-8


__author__ = 'gomi'

import HTMLParser, sys, urllib, base64

tagstack = []
html_ans = []


class ShowStructure(HTMLParser.HTMLParser):
    def handle_starttag(self, tag, attrs):
        tagstack.append(tag)

    def handle_endtag(self, tag):
        tagstack.pop()

    def handle_data(self, data):
        if data.strip():
            for tag in tagstack:
                sys.stdout.write('/' + tag)
            if tag == 'title':
                html_ans.append(data.strip())
            if tag == 'pre':
                html_ans.append(data.strip())
            sys.stdout.write(' >> %s\n' % data.strip())


def decode_base64(data):
    """Decode base64, padding being optional.

    :param data: Base64 data as an ASCII byte string
    :returns: The decoded byte string.

    """
    missing_padding = 4 - len(data) % 4
    if missing_padding:
        data += b'=' * missing_padding
    return base64.decodestring(data)

try:
    params = urllib.urlencode({'u': sys.argv[1]})
except IndexError:
    print u'请输入正确的参数'
    sys.exit(0)

f = urllib.urlopen("http://zxing.org/w/decode?%s" % params)

ans = f.read()

ShowStructure().feed(ans)

if html_ans[0] == 'Decode Succeeded':
    print ''
    server_info_all = decode_base64(html_ans[-1][5:])
    server_info = server_info_all.split(':')
    print u'加密方式:' + server_info[0]
    server_user = server_info[1].split('@')
    print u'地址:' + server_user[1]
    print u'密码:' + server_user[0]
    print u'远程端口:' + server_info[2]


