#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author    : zhaofy
# @Datetime  : 2020/11/9 14:10
# @File      : logger.py
# @desc      : 日志封装
import logging
from common.path_os import file_path
from functools import wraps


class Mylog:
    log_path = file_path().get_log_path()

    def __init__(self, logger):
        '''
            指定保存日志的文件路径，日志级别，以及调用文件
            将日志存入到指定的文件中
        '''
        # 创建一个logger
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)
        # 输出到文件
        fh = logging.FileHandler(self.log_path, 'a', encoding='utf-8')
        fh.setLevel(logging.INFO)

        # 输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s - %(name)s[line:%(lineno)d] - %(levelname)s : %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def getlog(self):
        return self.logger


logger = Mylog('logger').getlog()


def loggermate(param):
    def wrap(function):
        @wraps(function)
        def _wrap(*args, **kwargs):
            logger.info("当前模块 {}".format(param))
            logger.info("全部args参数参数信息 , {}".format(str(args)))
            logger.info("全部kwargs参数信息 , {}".format(str(kwargs)))
            return function(*args, **kwargs)
        return _wrap
    return wrap


if __name__ == '__main__':
    logger = Mylog('logger').getlog()
    logger.debug("world")
