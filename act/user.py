# coding=utf-8


class user:
    def __init__(self,user_id,subscribe_date):
        self.user_id=user_id
        self.subscribe_date=subscribe_date
        self.create_act_list=[]
        self.join_act_list=[]
        self.last_act_id=-1
        self.state=0