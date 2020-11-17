#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author    : zhaofy
# @Datetime  : 2020/7/24 17:42
# @File      : dbUtils.py
# @desc      :


import psycopg2
import pymysql
import redis
from common.logger import Mylog
from common.configUtils import ConfigUtils

log = Mylog('dbUtils.py').getlog()


class PostgreConn:
    '''Postgre数据库sql操作'''

    def __init__(self, env):
        self.env = env
        if 'test' in self.env:
            self.DBconn = ConfigUtils().get_config_dict('test_database')
        elif 'pre' in self.env:
            self.DBconn = ConfigUtils().get_config_dict('pre_database')
        else:
            raise ValueError('postgre配置查询错误！请检查conf文件env配置')

    def SelectOperate(self, sql):
        conn = psycopg2.connect(database="jhsaas", user=self.DBconn['user'], password=self.DBconn['password'],
                                host=self.DBconn['host'], port=self.DBconn['port'])
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        log.info('Sql查询结果：{}'.format(rows))
        conn.close()
        return rows


class mysqlconn:
    '''mysql数据库sql操作'''
    def __init__(self):
        self.host = ConfigUtils().get_config_value('mysql', 'host')
        self.user = ConfigUtils().get_config_value('mysql', 'user')
        self.password = ConfigUtils().get_config_value('mysql', 'password')

    def connect_mysql(self, database, sql):
        connect = pymysql.connect('192.168.200.104', self.user, self.password, database, port=3306)
        cursor = connect.cursor()
        # 执行sql
        cursor.execute(sql)
        # 获取执行结果,fetchone:获取一条；fetchall：获取所有
        result = cursor.fetchall()
        cursor.close()
        # 关闭数据库连接
        connect.close()
        return result


class RedisConn:
    '''redis数据库查询操作'''
    def __init__(self, env):
        self.env = env
        if 'test' in self.env:
            self.redisconn = ConfigUtils().get_config_dict('test_redis')
        elif 'pre' in self.env:
            self.redisconn = ConfigUtils().get_config_dict('pre_redis')
        else:
            raise ValueError('redis配置查询错误！请检查conf文件env配置')

    def redis_conn(self, key):
        conn = redis.Redis(host=self.redisconn['host'], port=self.redisconn['port'], password=self.redisconn['password'], db=1)
        result = conn.get(key)
        return result

    def get_img_verify(self, key):
        # 获取图片验证码
        b = str(self.redis_conn('saas:captcha:' + key))[-5:-1]
        ConfigUtils().write_config('Base', 'ImgCode', str(b))
        log.info('图片验证码：{}，写入conf文件成功！'.format(b))
        return b

    def get_phone_verify(self, phone):
        # 获取手机短信验证码
        b = self.redis_conn('ssxq:PIN:' + phone)
        log.info('短信验证码：{}'.format(int(b)))
        return b


if __name__ == '__main__':
    a = RedisConn('test').get_phone_verify('17777777771')
    print(a)
