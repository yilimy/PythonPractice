# -*- coding=utf-8 -*-

from urllib import request
import random
import json
import threading
import time
from subprocess import call
# import win32gui

# from win_notify import TestTaskbarIcon

# 需要python3环境

HEADER = {
    'Content-Type': 'application/json'
}

# taskbar = TestTaskbarIcon()


def request_data():
    url = 'http://www.wkj.link/ajax/allcoin_a/id/c?t=%s' % random.random()
    print(url)
    req = request.Request(url, headers=HEADER)
    try:
        data = request.urlopen(req, timeout=15.0).read()
        # print(data)
        # parse_data(data)
        # ====
        # f(data)
        # ====
        return json.loads(data.decode(), strict=False)
        # cnys = array['url']['btr_cny']
        # print(get_current_time())
        # print(cnys)
        # print("\n")
        # msg = "%s\n ===> %s" % (cnys[0], cnys[1])
    except Exception as e:
        # print("request eeror .")
        return []
    pass


def parse_all(array):
    l = array['url'];
    result = []
    for item in l.values():
        # print(item[0] + " " + str(item[1]))
        name = item[0]
        position = name.find('(')
        result.append(name[:position] + " " + str(item[1]) + "\n")
    return ''.join(result)[:-1]
    pass


def parse_rice(data):
    # array = json.loads(data, strict=False)
    # array = json.loads(data.decode(), strict=False)
    # print(array)
    # cnys = array['url']['btr_cny']
    cnys = data['url']['btr_cny']
    print(get_current_time())
    print(cnys)
    print("\n")
    # print("最新情报 --> %s %s" % (cnys[0], cnys[1]))
    # notify_mac("%s\n ===> %s" % (cnys[0], cnys[1]))
    # notify_win(str(cnys[0]), str(cnys[1]))
    return "%s\n ===> %s" % (cnys[0], cnys[1])
    pass


# 提示信息
def notify_mac():
    msg = parse_rice(request_data())
    cmd = 'display notification \"' + msg + '\" with title \"Dear Master\"'
    call(["osascript", "-e", cmd])
    pass
    
def notify_win(title, msg):
    # 通过这种方式，可能会导致右下角多个小窗口
    # 可以把class转进来
    taskbar.showMsg(title, get_current_time() + "\n当前价格 :  " + msg)  
    time.sleep(5)
    pass


def get_current_time():
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))


if __name__ == '__main__':
    # request_data(notify_mac)
    while True:
        t = threading.Thread(target=notify_mac)
        t.setDaemon(True)
        t.start()
        # 每10分钟执行一次
        time.sleep(600)
    pass
