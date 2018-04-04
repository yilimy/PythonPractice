# -*- coding:utf-8 -*-
import queue
import threading
from urllib import request
import json
from qqbot import _bot as bot
import time

# 丰登街没有关注达人的选项，错过消息了怎么办？
# 目标是定期轮询新消息，祝大家涨涨涨~
# 需要python 3 支持
# 需要QQbot支持：<a href="https://github.com/pandolia/qqbot"/>

# 要关注的对象
authors = ['一路向阳',]
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
# 给谁发消息
QQ_TARGET = ''
# 消息队列
q = queue.Queue()


# 发送请求并获取返回值
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


# 解析json数据
def parse_json(json_str):
    # 非严格校验时会有换行符出现，好的解决方式其实不是replace，而是使用数据库
    array = json.loads(json_str.replace('\n', ''), strict=False)
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

    response_data = list()
    for item in result_list:
        # 为了与文件内容一致，此处添加了换行符
        response_data.append('%s %s [%s] : %s\n' % (item['dateline'], item['author'], item['customstatus'], item['message']))

    # 发送给qq好友的消息
    qq_msg = ''
    f = open('result.txt', 'a+', encoding='utf8')
    # a+需要将读取指针置于开头
    f.seek(0)
    # 一次性读取文件所有数据
    lines = f.readlines()
    for item in response_data:
        if item not in lines:
            f.write(item)
            print('您有新消息:')
            print(item)
            qq_msg += item
    # 去掉最后一行的换行符
    q.put(qq_msg.strip('\n'))
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ' Done !')
    f.flush()
    f.close()


# 通过QQ发送消息
def send_msg_by_qq(msg):
    if msg:
        print('发送消息给 %s ' % QQ_TARGET)
        bl = bot.List('buddy', QQ_TARGET)
        if bl:
            b = bl[0]
            bot.SendTo(b, msg)


# 执行的线程任务
def thread_run():
    string = request_data()
    parse_json(string)


# 每隔1分钟执行一次请求线程
def manager_run():
    # 轮询：每隔一分钟
    while True:
        time.sleep(1)
        t = threading.Thread(target=thread_run)
        t.setDaemon(True)
        t.start()
        time.sleep(60)
    pass


if __name__ == '__main__':
    QQ_TARGET = input('请输入发送消息给谁(QQ号):\n')
    bot.Login(['-q', '1234'])
    # thread_run()
    t = threading.Thread(target=manager_run)
    t.setDaemon(True)
    t.start()
    # 随时准备给qq好友发送消息
    while True:
        if not q.empty():
            send_msg_by_qq(q.get())
