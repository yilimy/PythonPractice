# -*- coding:utf-8 -*-

from urllib import request
import json

# 丰登街没有关注达人的选项，错过消息了怎么办？
# 目标是定期轮询新消息，祝大家涨涨涨~

# 要关注的对象
authors = ['一路向阳']
# 要关注的头衔
customstatus = ['活跃街友', '奔跑达人', '股市达人']

# 圈子地址
URL = 'http://fengdengjie.com/interface.php?action=topiclist'
# 边界
BOUNDARY = '0xKhTmLbOuNdArY-956E55F5-FCAE-4B4C-A99A-CBCEA90A8D68'
# 请求头
HEADER = {
'Host':'fengdengjie.com',
'Content-Type':'multipart/form-data; charset=utf-8;boundary=%s' % BOUNDARY,
'Content-Length':214
}


def request_data():
    data = list()
    data.append('--%s' % BOUNDARY)
    data.append('Content-Disposition: form-data; name="jsonstr"')
    data.append('\r\n')
    # fid 和 uid 是什么呢？
    data.append('{"fid":"37","uid":"551297","tid":"0","kind":"0"}')
    data.append('--%s--' % BOUNDARY)

    http_body = bytes('\r\n'.join(data), encoding='utf-8')

    req = request.Request(URL, data=http_body, headers=HEADER)
    data = request.urlopen(req).read()

    return data.decode('unicode_escape')


def parse_json(json_str):
    array = json.loads(json_str)
    # print(array)
    result_list = []
    for item in array:
        # item is a dict
        if item['author'] in authors:
            result_list.append(item)
            continue
        if item['customstatus'] in customstatus:
            result_list.append(item)
            continue
        pass

    # 时间降序：最近的在上面
    result_list.sort(key=lambda d: d['dateline'], reverse=True)
    # 时间升序：最近的在下面
    # list.sort(key=lambda d: d['dateline'])

    for item in result_list:
        print('%s %s [%s] : %s' % (item['dateline'], item['author'], item['customstatus'], item['message']))


if __name__ == '__main__':
    string = request_data()
    parse_json(string)
