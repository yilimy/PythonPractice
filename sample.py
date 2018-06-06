# -*- coding: utf-8 -*-

from subprocess import call

# 基于qqbot的监控qq群消息的插件
# 位于 ~/.qqbot-tmp/

# 插件加载方法： 
# 先运行 qqbot ，启动成功后，在另一个命令行窗口输入： qq plug qqbot.plugins.sample

def onQQMessage(bot, contact, member, content):
    # if content == '-hello':
    #     bot.SendTo(contact, '你好，我是QQ机器人')
    # elif content == '-stop':
    #     bot.SendTo(contact, 'QQ机器人已关闭')
    #     bot.Stop()
    if "比特米" in content:
        try:
            # 添加一个英文字符"."为了防止中文结尾乱码
            content +='.'
            start = content.index("比特米")
            end = content.index("播控云")
            str = content[start:end]
            command(str)
        except Exception as e:
            print(e)
        
def command(str):
    cmd = 'display notification \"' + str + '\" with title \"Dear Master\"'
    call(["osascript", "-e", cmd])
