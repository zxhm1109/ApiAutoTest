#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author    : zhaofy
# @Datetime  : 2020/7/21 15:45
# @File      : redis_connect.py
# @desc      :

import redis
from common.DoConfig import *
from common.logger import Mylog

logger = Mylog()


def redis_conn(key):
    host = ReadConfig.read_config('redis', 'host')
    password = ReadConfig.read_config('redis', 'password')
    conn = redis.Redis(host=host, port=6379, password=password)
    access_token = conn.get(key)
    return access_token


def get_img_code(key):
    # 获取图片验证码
    b = str(redis_conn(key))[-5:-1]
    WriteConfig.write_config('Base', 'ImgCode', str(b))
    logger.info('图片验证码：{}，写入conf文件成功'.format(b))
    return b


if __name__ == '__main__':
    a = redis_conn('DEFAULT_CODE_KEY:7BB31FC6-E054-4698-82FC-FF284794F66C')
    print(str(a)[-5:-1])
