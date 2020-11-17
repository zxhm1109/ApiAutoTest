#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author    : zhaofy
# @Datetime  : 2020/7/22 10:11
# @File      : To_Emil.py
# @desc      :

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from common.configUtils import ConfigUtils
from common.logger import Mylog

logger = Mylog('To_Emil.py').getlog()

my_sender = ConfigUtils().get_config_value('Email', 'my_sender')
my_pass = ConfigUtils().get_config_value('Email', 'my_pass')
my_user = ConfigUtils().get_config_value('Email', 'my_user')


def ToEmail(sendmsg):
    try:
        # 配置发送内容
        msg = MIMEText(sendmsg, 'html', 'utf-8')
        msg['From'] = formataddr(("TEST", my_sender))
        msg['To'] = formataddr(("api-test", my_user))
        msg['Subject'] = "发送邮件测试"
        # 邮箱配置
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)
        # 通过授权码登陆邮箱
        server.login(my_sender, my_pass)
        # 发送邮件
        server.sendmail(my_sender, [my_user, ], msg.as_string())
        server.quit()
        logger.info("邮件发送成功")
        return True
    except Exception as e:
        logger.error("邮件发送失败:{}".format(e))
        return False


if __name__ == '__main__':
    aaa = '''<html><a href="https://www.runoob.com/" target="_blank" rel="noopener noreferrer">访问菜鸟教程!</a></html>'''
    ret = ToEmail(aaa)
