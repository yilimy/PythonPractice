# -*- coding:utf-8 -*-

from qqbot import _bot as bot
import time
import threading
import queryBTR
import queue

# 给谁发消息
# QQ_TARGET_BTR = 'Myl'
QQ_TARGET_BTR = '流浪的云'


# 通过QQ发送消息
def send_msg_by_qq(msg):
    if msg:
        print('发送消息给 %s ' % QQ_TARGET_BTR)
        bl = bot.List('buddy', QQ_TARGET_BTR)
        if bl:
            b = bl[0]
            bot.SendTo(b, msg)


def manager_run():
    arr = queryBTR.request_data()
    msg = queryBTR.parse_all(arr)
    send_msg_by_qq(msg)
    # send_msg_by_qq("test")
    # queryBTR.request_data(queryBTR.notify_mac)
    pass

if __name__ == '__main__':
    # QQ_TARGET_BTR = input('请输入发送消息给谁(QQ号):\n')
    # 扫描二维码登录
    bot.Login(['-q', '1234'])
    # qqbot启动时间
    time.sleep(3)
    while True:
        # qq消息必须在主线程
        manager_run()
        time.sleep(7)
        pass
    # while True:
    #     t = threading.Thread(target=manager_run)
    #     t.setDaemon(True)
    #     t.start()
    #     time.sleep(7)
    # pass
