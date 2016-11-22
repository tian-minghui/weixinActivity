# coding=utf-8
import time


def get_time():
    TIMEFORMAT = '%Y-%m-%d %X'
    return time.strftime(TIMEFORMAT)


def time_sec_to_str(time_sec):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_sec))