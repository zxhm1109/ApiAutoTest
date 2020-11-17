# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# # @Author    : zhaofy
# # @Datetime  : 2020/11/2 14:02
# # @File      : login.py
# # @desc      :
#
# import requests
# from common.DoExcel import get_excel_base_wite_conf
# from http import cookiejar
# from urllib import request
#
# # 声明一个CookieJar对象实例来保存cookie
# cookie = cookiejar.CookieJar()
# # 利用urllib.request库的HTTPCookieProcessor对象来创建cookie处理器,也就CookieHandler
# handler = request.HTTPCookieProcessor(cookie)
# # 通过CookieHandler创建opener
# opener = request.build_opener(handler)
# # 此处的open方法打开网页
# response = opener.open('http://www.baidu.com')
#
# url = 'https://t2wxapi.sancell.top/saas-back/b/auth/captchaDataUri'
# header = get_excel_base_wite_conf()
# print(header)
# print(header['User-Agent'])
# result = requests.get(url, header)
# captchaId = result.json()['content']['captchaId']
# from common.redis_connect import RedisConn
#
# verify = RedisConn('test').get_img_verify(captchaId)
#
# url2 = 'https://t2wxapi.sancell.top/saas-back/b/auth/syslogin'
# data = {
#     "loginMethod": "PASSWORD_LOGIN",
#     "phoneNumber": "",
#     "smsCode": "",
#     "userCode": "zhaofy",
#     "userPassword": "c2c2759689821d1190f10bd9a7caabf5",
#     "captcha": verify,
#     "captchaId": captchaId,
#     "user_auto": "ENABLE",
#     "loginType": "PLAT",
#     "type": "JSON"
# }
# result2 = requests.post(url2, data)
# print(result2.text)
# cookie = result2.cookies
# print('1111111111', type(cookie))
#
# url1 = 'https://t2wxapi.sancell.top/ssxqAdmin/back/identify/batchList'
# result1 = requests.get(url1, header, cookies=cookie)
# print('1231231212', result1.text)
# print()
# print('33333333', result1.cookies, end=' ')
#
# if __name__ == '__main__':
#     a = [1, 2, 3]
#     b = [3, 2, 1]
#     if a == b:
#         print(11)
#     else:
#         print(222)



# import logging,os,time
# from common.path_os import file_path
# class loggingComdat():
#     def __init__(self):
#
#         self.logger = logging.getLogger('root')  #初始化日志对象
#         self.logger.setLevel('DEBUG') #设定日志的信息级别
#         #设定控制台输出日志信息
#         console_log = logging.StreamHandler() #初始化控制台信息
#         console_log.setLevel('debug')
#         simple_formatter = logging.Formatter('%(asctime)s %(name)s[line:%(lineno)d] %(levelname)s-> %(message)s') #初始化日志格式
#         console_log.setFormatter(simple_formatter) #设定日志格式
#         self.logger.addHandler(console_log)  #将控制台作为日志输出通道
#
#         #设定日志输出到日志文件
#         #设计日志文件的名字
#         now = time.strftime('%y-%m-%d',time.localtime())
#         file_name = 'test_result_%s.log'%now
#         log_file_name = file_path().get_log_path()
#         self.file_log = logging.FileHandler(log_file_name,encoding='utf-8')  #初始化日志文件
#         self.file_log.setLevel('debug')
#         normal_formatter = logging.Formatter('%(asctime)s %(name)s[line:%(lineno)d] %(levelname)s-> %(message)s') #初始化日志格式
#         self.file_log.setFormatter(normal_formatter) #将日志格式应用到日志文件中
#         self.logger.addHandler(self.file_log) #将日志文件作为日志输出通道
#
#     def get_logger(self):
#         return self.logger
#
#     def close_log(self):
#         self.logger.removeHandler(self.file_log)  #移除日志输出
#         self.file_log.close()
#
# do_logger = loggingComdat().get_logger()
#
# if __name__ == '__main__':
#
#     do_logger.error('这是一个错误')
#     do_logger.info('这是一个正确的信息')