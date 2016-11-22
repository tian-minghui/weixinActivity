# coding=utf-8

import urllib2
# import urllib
from Contant import APPID,APPSECRET,MENU
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


access_token="I6-cIxDex7duOdC2guHhDWQftd9doaFw6GOo_JoSj3EOqvtZ5MOUqbgwWzglNL-yPZvzf3RKVqFpDQz9d9q0L1TnOoHJCWAQa4jKk27HSRsYXFaAGAFEM"
errcode_token=[42001,41001,40014]

def update_token():
    global access_token
    url='https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s'%(APPID,APPSECRET)
    req=urllib2.Request(url)
    response=urllib2.urlopen(req)
    content=response.read()
    info=json.loads(content)   # 从json格式的字符串转化为python数据类型
    if "errcode" in info.keys():
        raise KeyError('更新token出错：%s'%info.get("errcode"))
    access_token=info.get('access_token')


def update_menu():
    # headers = {
    #     'Content-Type': 'application/json',
    #     'encoding':'utf-8'
    # }
    # print access_token
    url="https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s"%access_token
    req=urllib2.Request(url)
    req.add_header('Content-Type', 'application/json')
    req.add_header('encoding', 'utf-8')
    response=urllib2.urlopen(req,json.dumps(MENU,ensure_ascii=False))  # 从python数据类型转换为json类型的字符串
    info = json.loads(response.read())
    errcode=info.get('errcode')
    if errcode==0:
        print '更新菜单成功'
    elif errcode in errcode_token:
        update_token()
        update_menu()
    else:
        raise RuntimeError('更新菜单出错：%d'%errcode)


def get_user_info(userid):
    url='https://api.weixin.qq.com/cgi-bin/user/info?access_token=%s&openid=%s&lang=zh_CN'%(access_token,userid)
    response=urllib2.urlopen(url)
    info=json.loads(response.read())
    if 'errcode' in info.keys():
        errcode=info.get('errcode')
        if errcode in errcode_token:
            update_token()
            return get_user_info(userid)
        else:
            raise RuntimeError('获取用户信息出错：%d' % errcode)
    else:
        subscribe=info.get('subscribe')
        nickname=info.get('nickname')
        if subscribe==1:
            return nickname
        else:
            raise NameError('非关注用户或者id非法')


def get_mutiluser_info(userid_list):
    url='https://api.weixin.qq.com/cgi-bin/user/info/batchget?access_token=%s'%access_token
    dic_json={
        "user_list":[]
    }
    for userid in userid_list:
        dic_json['user_list'].append({'openid':userid, "lang": "zh-CN"})

    req=urllib2.Request(url)
    req.add_header('Content-Type', 'application/json')
    req.add_header('encoding', 'utf-8')
    response=urllib2.urlopen(req,json.dumps(dic_json))
    info=json.loads(response.read())
    if 'errcode' in info.keys():
        errcode = info.get('errcode')
        if errcode in errcode_token:
            update_token()
            return get_mutiluser_info(userid_list)
        else:
            raise RuntimeError('获取用户列表信息出错：%d' % errcode)
    else:
        name_list=[]
        for user in info.get('user_info_list'):
            if user.get('subscribe')==1:
                # openid=user.get('openid')
                nickname= user.get('nickname')
                name_list.append(nickname)
        return name_list


if __name__ == '__main__':
    print get_mutiluser_info(['o6ngQv5DAxoOoABubGsPCYLynFFc','o6ngQv2BwJipHSaHN8_m-RTTT3nw'])