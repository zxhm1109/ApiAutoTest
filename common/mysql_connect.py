#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author    : zhaofy
# @Datetime  : 2020/6/18 21:43
# @File      : mysql_connect.py
# @desc      :
from common.DoConfig import ReadConfig

import pymysql


class mysql:
    def __init__(self):
        self.host = ReadConfig.read_config('mysql', 'host')
        self.user = ReadConfig.read_config('mysql', 'user')
        self.password = ReadConfig.read_config('mysql', 'password')

    def connect_mysql(self, database, sql):
        connect = pymysql.connect(self.host, self.user, self.password, database, charset='utf-8')
        cursor = connect.cursor()
        cursor.executr(sql)
        result = cursor.fetchall()
        cursor.close()
        # 关闭数据库连接
        connect.close()
        return result
