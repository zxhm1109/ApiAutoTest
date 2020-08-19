#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author    : zhaofy
# @Datetime  : 2020/6/23 12:02
# @File      : only_run.py
# @desc      :


# import requests
# import datetime, time
#
# url = r'http://192.168.200.104:9900/api-user/users/current'
# start_time = datetime.datetime.now()
#
# oo = 600
# token = 'c6c9deef-176f-49ca-93fc-5323ef0f50e8'
# header = {"Authorization": "Bearer " + token}
# res = True
# while res:
#     print('-----------开始：{}--------------'.format(datetime.datetime.now()))
#     result = requests.get(url, headers=header)
#     if result.json()['resp_code'] != 0:
#         end_time = datetime.datetime.now()
#         print(result.json()['resp_code'])
#         print('-----------结束：{}--------------'.format(datetime.datetime.now()))
#         print('耗时：{}'.format(end_time - start_time))
#         res = False
#         break
#     else:
#         print(result.json()['resp_code'])
#         oo += 600
#     time.sleep(oo)
a = ' '
b = 'resp_code=0,resp_msg=验证码不存在或已过期'
c='resp_code=0'

def Assert(expected):
    exp={}
    if expected.strip():
        for i in expected.split(','):
            exp[i.split('=')[0]]=i.split('=')[1]
        print(exp)
    else:
        print('2')


Assert(b)
