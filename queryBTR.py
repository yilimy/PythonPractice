# -*- coding=utf-8 -*-

from urllib import request
import random
import json
import threading
import time
from subprocess import call
import win32gui

from win_notify import TestTaskbarIcon

# 需要python3环境

HEADER = {
    'Content-Type': 'application/json'
}

taskbar = TestTaskbarIcon()

def request_data():
    url = 'http://www.wkj.link/ajax/allcoin_a/id/c?t=%s' % random.random()
    print(url)
    req = request.Request(url, headers=HEADER)
    data = request.urlopen(req).read()
    print(data)
    parse_data(data)
    pass


def parse_data(data):
    # array = json.loads(data, strict=False)
    array = json.loads(data.decode(), strict=False)
    print(array)
    cnys = array['url']['btr_cny']
    print(cnys)
    # print("最新情报 --> %s %s" % (cnys[0], cnys[1]))
    # notify("%s --> %s" % (cnys[0], cnys[1]))
    notify_win(str(cnys[0]), str(cnys[1]))
    pass


# 提示信息
def notify_mac(msg):
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
    while True:
        t = threading.Thread(target=request_data)
        t.setDaemon(True)
        t.start()
        # 每10分钟执行一次
        time.sleep(600)
    pass
