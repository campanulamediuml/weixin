#!/usr/bin/env python
# coding: utf-8

from wxbot import *
import ConfigParser
import json
from random import randint, shuffle
import os
import codecs
import re
from sopel.tools.calculation import eval_equation as eval2
import dicebot
import method

class TulingWXBot(WXBot):
    def __init__(self):
        WXBot.__init__(self)

        self.tuling_key = ""
        self.robot_switch = True
        self.trigger_list = ['.roll','.help','.r','.class','.8ball','.zhan','.fate', '.calc', '.choice','.tips']
        self.class_files = self.list_classfiles("class" )
        fate_file = codecs.open("fate.list", encoding='utf-8')
        self.fate_list = []
        for i in fate_file.readlines():
            self.fate_list.append(i)

        fate_file.close()
        fate_file = codecs.open("zhan.list", encoding='utf-8')
        self.zhan_list = []
        for i in fate_file.readlines():
            self.zhan_list.append(i)

        fate_file.close()

        try:
            cf = ConfigParser.ConfigParser()
            cf.read('conf.ini')
            self.tuling_key = cf.get('main', 'key')
        except Exception:
            pass
        print 'tuling_key:', self.tuling_key

    def list_classfiles(self,class_path="class"):
        filelist = []
        for (dirpath,dirnames,filenames) in os.walk(class_path):
            for files in filenames:
                #print files
                filelist.append(str(files).decode('utf-8'))
            break
        return filelist

    def tuling_auto_reply(self, uid, msg):
        # deal with messages from here...
        #return u"知道啦"
        content = msg.lower()
        
        if content == './reload':
            try:
                imp.reload(method)
                result = u'成功编译完成'
            except Exception, e:
                print e
                result = u'指令库更新失败，请查看日志'

        elif content[:2] = './':
            result = str(method.auto_reply(content))

        else:
            result = empty_reply[0]

        print '    ROBOT:', result
        return result


    def auto_switch(self, msg):
        msg_data = msg['content']['data']
        stop_cmd = [u'退下', u'走开', u'关闭', u'关掉', u'休息', u'滚开']
        start_cmd = [u'出来', u'启动', u'工作']
        if self.robot_switch:
            for i in stop_cmd:
                if i == msg_data:
                    self.robot_switch = False
                    self.send_msg_by_uid(u'[Robot]' + u'机器人已关闭！', msg['to_user_id'])
        else:
            for i in start_cmd:
                if i == msg_data:
                    self.robot_switch = True
                    self.send_msg_by_uid(u'[Robot]' + u'机器人已开启！', msg['to_user_id'])

    def handle_msg_all(self, msg):
        if not self.robot_switch and msg['msg_type_id'] != 1:
            return
        if msg['msg_type_id'] == 1 and msg['content']['type'] == 0:  # reply to self
            self.auto_switch(msg)
        elif msg['msg_type_id'] == 5 and msg['content']['type'] == 0:  # text message from contact
            self.send_msg_by_uid(self.tuling_auto_reply(msg['user']['id'], msg['content']['data']), msg['user']['id'])
        elif msg['msg_type_id'] == 3 and msg['content']['type'] == 0:  # group text message
            if 'detail' in msg['content']:
                message_text = msg['content']['desc'] 
                src_name = msg['content']['user']['name']
                #print '>' +  message_text
                #print msg['content']['user']
                if any(trigger_item in message_text.lower() for trigger_item in self.trigger_list):
                    reply = ''
                    #print 'name: ' + src_name
                    if msg['content']['type'] == 0:  # text message
                        #reply += self.tuling_auto_reply(msg['content']['user']['id'], msg['content']['desc'])
                        reply += self.tuling_auto_reply(msg['user']['id'], msg['content']['desc'])
                    else:
                        reply += u"对不起，只认字，其他杂七杂八的我都不认识，,,Ծ‸Ծ,,"

                    if reply:
                        reply = 'to ' + src_name + ': ' + reply
                        self.send_msg_by_uid(reply, msg['user']['id'])


def main():
    bot = TulingWXBot()
    bot.DEBUG = False #True
    bot.conf['qr'] = 'tty'

    bot.run()


if __name__ == '__main__':
    main()

