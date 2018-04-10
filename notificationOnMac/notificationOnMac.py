# -*- coding:utf-8 -*-

import time
from subprocess import call

# 每隔45分钟提醒一次
DURING = 60 * 45


def command():
    cmd = 'display notification \"' + \
          "It is time to have a rest ." + '\" with title \"Dear Master\"'
    call(["osascript", "-e", cmd])

if __name__ == '__main__':
    while True:
        command()
        # 据观察mac的提示持续时间在5秒左右
        time.sleep(10)
