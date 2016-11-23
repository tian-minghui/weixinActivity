# coding=utf-8
import sql
import time
import sys
import weixinutil
import tools
reload(sys)
sys.setdefaultencoding('utf-8')


class activity:
    def __init__(self,act_id):
        self.act_id=act_id   # 活动id
        self.create_userid=''  # 活动创建人
        self.title=''   # 活动标题
        self.date=0   # 活动创建日期
        self.num=1   # 已参与人数
        self.id_list=[]  # 参与人id
        self.remark=''  # 活动备注


def md_act_id(act_id):
    id_length=6
    s=str(act_id)
    id=''
    for i in range(id_length-len(s)):
        id+='0'
    return id+s


def create_act(userid,content):
    # 创建活动
    l=content.split()
    if len(l)!=3:
        # msg=str(len(l))
        # for i in l:
        #     msg+=i
        return '你输入的信息格式有误！'
    else:
        title=l[1]
        remark=l[2]
        act_id= sql.mysql().get_max_actid() + 1
        act= activity(act_id)
        act.title=title
        act.num=1
        act.date=time.time()
        act.remark=remark
        # 插入表
        act.id_list.append(userid)
        act.create_userid=userid
        sql.mysql().insert_act(act)
        # 更新user表
        u= sql.mysql().select_user(userid)
        u.create_act_list.append(act_id)
        sql.mysql().update_user(u, flag=0)
        return md_act_id(act_id)


def show_act(act):
    create_name=weixinutil.get_user_info(act.create_userid)
    join_name_list=weixinutil.get_mutiluser_info(act.id_list)
    msg='''活动标题：%s
活动id:%s
备注：%s
创建人：%s
创建日期：%s
参与人数：%d
报名人:
%s
'''%(act.title,md_act_id(act.act_id),act.remark,create_name,tools.time_sec_to_str(act.date),act.num,' '.join(join_name_list))
    return msg


def join_act(userid,content):
    l=content.split()
    if len(l)!=2:
        return '你输入的信息格式有误！'
    act= sql.mysql().select_act(int(l[1]))
    if act==None:
        return '没有此活动号,请确认活动号！'
    if userid in act.id_list:
        return '你已报名此活动！'
    act.id_list.append(userid)
    sql.mysql().update_act(act, id_list=True)
    u= sql.mysql().select_user(userid)
    u.join_act_list.append(act.act_id)
    sql.mysql().update_user(u, flag=1)
    return show_act(act)

if __name__ == '__main__':
    print md_act_id(1)