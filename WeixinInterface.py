# coding=utf-8
import web
import os
from Contant import Token
import hashlib
from xml.etree import ElementTree
import response


class WeixinRequest:  # 响应请求的类
    def __init__(self):
        self.root_path=os.path.dirname(__file__)
        self.templates_path=os.path.join(self.root_path,'templates')
        self.render=web.template.render(self.templates_path)

    def GET(self):  # 微信开发者验证
        data=web.input()
        signature = data.signature
        timestamp = data.timestamp
        nonce = data.nonce
        echostr = data.echostr
        l=[timestamp,Token,nonce]
        l.sort()
        sha1=hashlib.sha1()
        map(sha1.update,l)
        if sha1.hexdigest()==signature:
            return echostr

    def POST(self):  # 用户请求
        data=web.data()
        xml=ElementTree.fromstring(data)
        msgtype=xml.find("MsgType").text
        userid=xml.find("FromUserName").text
        myid=xml.find("ToUserName").text

        if msgtype=="text":
            content=xml.find("Content").text
            return response.resp_text(self.render,myid,userid,content)
        elif msgtype=="event":
            event = xml.find("Event").text
            if event=='subscribe' or event=='unsubscribe':
                return response.resp_event(self.render,event,myid,userid)
            elif event=='CLICK':
                eventkey = xml.find('EventKey')
                return response.resp_menu_event(self.render,myid,userid,eventkey.text)