# coding=utf-8
import MySQLdb
from sae.const import MYSQL_DB,MYSQL_USER,MYSQL_PASS,MYSQL_HOST,MYSQL_PORT

from act import activity, user

'''
sae.const.MYSQL_DB      # 数据库名
sae.const.MYSQL_USER    # 用户名
sae.const.MYSQL_PASS    # 密码
sae.const.MYSQL_HOST    # 主库域名（可读写）
sae.const.MYSQL_PORT    # 端口，类型为<type 'str'>，请根据框架要求自行转换为int
sae.const.MYSQL_HOST_S  # 从库域名（只读）
'''

conn=MySQLdb.connect(
    host=MYSQL_HOST,
    port=MYSQL_PORT,
    user=MYSQL_USER,
    passwd=MYSQL_PASS,
    db=MYSQL_DB
)
cur=conn.cursor()


def create_act_table():
    sql='''create table IF NOT EXISTS Activity(
act_id int(10) NOT NULL UNIQUE ,
create_userid VARCHAR(50) ,
title VARCHAR(30) not NULL ,
date FLOAT NOT null,
num int not NULL ,
id_list TEXT,
remark varchar(100))'''
    cur.execute(sql)


def create_user_table():
    sql='''create table if not EXISTS user(
user_id varchar(50) not NULL ,
subscribe_date FLOAT ,
create_act_list TEXT ,
join_act_list TEXT ,
state int,
last_act_id VARCHAR(50))'''
    cur.execute(sql)


def insert_act(act):
    str_id_list=' '.join(act.id_list)
    sql="insert into Activity VALUE (%d,'%s','%s',%f,%d,'%s','%s')"%(act.act_id,act.create_userid,act.title,act.date,act.num,str_id_list,act.remark)
    cur.execute(sql)


def get_max_actid():
    sql='select max(act_id) from Activity'
    count=cur.execute(sql)
    if count==0:
        return 0
    id = cur.fetchall()[0][0]
    return int(id)


def update_act(act,title=False,id_list=False,remark=False):
    if title:
        sql="update Activity set title='%s' where act_id=%d"%(act.title,act.act_id)
        cur.execute(sql)
    if id_list:
        sql = "update Activity set id_list='%s',num=%d where act_id=%d" % (act.id_list, act.num+1,act.act_id)
        cur.execute(sql)
    if remark:
        sql = "update Activity set remark='%s' where act_id=%d" % (act.remark, act.act_id)
        cur.execute(sql)


def select_act(act_id):
    sql="select * from Activity where act_id=%d"%act_id
    count=cur.execute(sql)
    if count==0:
        return
    result=cur.fetchall()[0]
    act= activity.activity(act_id)
    act.title=result[1]
    act.date=result[2]
    act.num=result[3]
    act.id_list=result[4].split()
    act.remark=result[5]
    return act


def insert_user(u):
    str_act_list=' '.join(u.create_act_list)
    str_join_list=' '.join(u.join_act_list)
    sql="insert into user VALUE ('%s','%f','%s','%s',%d,%d)"%(u.user_id,u.subscribe_date,str_act_list,str_join_list,u.state,u.last_act_id)
    cur.execute(sql)


def select_user(user_id):
    sql="select * from user where user_id='%s'"%user_id
    cur.execute(sql)
    result=cur.fetchall()[0]
    u= user.user(user_id, float(result[1]))
    # u.subscribe_date=result[1]
    u.create_act_list=result[2].split()
    u.join_act_list=result[3].split()
    u.state=int(result[4])
    u.last_act_id=int(result[5])
    return u


def update_user(u,flag):
    # flag=0更新create_act_list   flag=1更新join_act_list
    if flag==0:
        str_act_list = ' '.join(u.create_act_list)
        sql="update user set create_act_list='%s',last_act_id=%d where user_id=%d"%(str_act_list,u.create_act_list[-1],u.user_id)
        cur.execute(sql)
    elif flag==1:
        str_join_list = ' '.join(u.join_act_list)
        sql = "update user set join_act_list='%s',last_act_id=%d where user_id=%d" % (str_join_list,u.join_act_list[-1], u.user_id)
        cur.execute(sql)


def delete_user(userid):
    sql="delete from user where user_id='%s'"%userid
    cur.execute(sql)
