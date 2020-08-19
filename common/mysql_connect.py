#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author    : zhaofy
# @Datetime  : 2020/6/18 21:43
# @File      : mysql_connect.py
# @desc      :
from common.DoConfig import ReadConfig

import pymysql


class mysql:
    host = ReadConfig.read_config('mysql', 'host')
    user = ReadConfig.read_config('mysql', 'user')
    password = ReadConfig.read_config('mysql', 'password')

    @classmethod
    def connect_mysql(cls, database, sql):
        connect = pymysql.connect('192.168.200.104', cls.user, cls.password, database, port=3306)
        cursor = connect.cursor()
        # 执行sql
        cursor.execute(sql)
        # 获取执行结果,fetchone:获取一条；fetchall：获取所有
        result = cursor.fetchall()
        cursor.close()
        # 关闭数据库连接
        connect.close()
        return result


if __name__ == '__main__':
    a = mysql().connect_mysql('ssxq-product-center', "select * from pc_category where id ='100202037'")
    print(a)
