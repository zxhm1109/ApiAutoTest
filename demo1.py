#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author    : zhaofy
# @Datetime  : 2020/7/1 16:01
# @File      : demo1.py
# @desc      :

import time
from selenium import webdriver
from common.logger import Mylog
from common.DoExcel import doexcel

'''获取新氧类目列表，并写入excel'''
logger = Mylog()
driver = webdriver.Chrome(r'C:\myworkfile\py_package\chromedriver.exe')
driver.get('https://www.soyoung.com/itemk/')
driver.maximize_window()
ele = driver.find_elements_by_xpath('//*[@class="con-1180 item-block"]')
bbb = {}
for i in ele:
    aaa = {}
    logger.info(
        '一级类目：{}'.format(i.find_element_by_class_name('tab-title').text, i.get_attribute('id')))
    for x in i.find_elements_by_class_name('second-item'):
        logger.info('二级类目:    {}'.format(x.text))
        try:
            x.click()
        except:
            elee = '//*[@id="{}"]/div[1]/div[2]/div/div[2]/div[3]'.format(i.get_attribute('id'))
            driver.find_element_by_xpath(elee).click()
            time.sleep(2)
            x.click()
        time.sleep(5)
        res = i.text
        if res is None:
            raise ValueError
        a = res.split('\n')
        san = {}
        for aa in a:
            if "¥" in aa:
                index = a.index(aa)
                logger.info('三级类目：       {} --{}'.format(aa[:aa.find('¥')], a[index + 1]))
                san[aa[:aa.find('¥')]] = a[index + 1]
        aaa[x.text] = san
    bbb[i.find_element_by_class_name('tab-title').text] = aaa
logger.info(bbb)
driver.close()
num = 1
filepath = r'C:\myworkfile\py_package\ApiAutoTest_demo\Config\category.xlsx'
for x, y in bbb.items():
    for q, w in y.items():
        for e, r in w.items():
            print("{} - {} - {}：{}".format(x, q, e, r))
            doexcel().write_excel(sheetname='Sheet1', row=num, col=1, value=x)
            doexcel().write_excel(sheetname='Sheet1', row=num, col=2, value=q)
            doexcel().write_excel(sheetname='Sheet1', row=num, col=3, value=e)
            doexcel().write_excel(sheetname='Sheet1', row=num, col=4, value=r)
            num += 1
if __name__ == '__main__':
    pass

''' excel读取历史版本
from openpyxl import load_workbook
import json
from common.DoConfig import ReadConfig
from common.logger import Mylog
from common.path_os import file_path
import pandas as pd
from pandas import DataFrame

log = Mylog()


class doexcel:
    host = ReadConfig.read_config('Base', 'host')
    casefile = file_path().get_case_path()

    def read_excel(self, sheetname):
        wb = pd.read_excel(self.casefile, sheet_name=sheetname)
        # 读取第一行,list
        # data = wb.loc[0].values
        # print(wb.index.values[5])
        case_data = []
        for i in wb.index.values:
            row_data = wb.loc[
                i, ['CaseId', 'Execute', 'CaseName', 'URL', 'Method', 'Header', 'Parameters', 'Responses', 'Expect', 'Reality'
                    ]].to_dict()
            row_data['sheetname'] = sheetname
            case_data.append(row_data)
        return case_data

    def get_sheet_title(self, name):
        wb = pd.read_excel(self.casefile, sheet_name=name, nrows=0)
        for i in wb.columns.values:
            print(wb.columns.values)


if __name__ == '__main__':
    from common.DoConfig import ReadConfig

    sheetname = ReadConfig.read_config_options_dict('sheetname')
    caselist = []
    doexcel().get_sheet_title('uaa')
    # for x, y in sheetname.items():
    #     data = doexcel().read_excel(x)
    #     caselist.append(data)
    # c = []
    # for i in caselist:
    #     c += i
    # print(c)
'''

'''日志历史版本

class Mylog:

    def my_log(self, msg, level):
        # 创建logger实例
        mylog = logging.getLogger('__main__')
        #设置日志等级
        mylog.setLevel(logging.DEBUG)

        # 定义日志输入格式
        formatter = logging.Formatter(
            '%(asctime)s %(filename)s->line:%(lineno)d %(levelname)s: %(message)s')

        # 设置日志输出位置
        cl = logging.StreamHandler()
        fl = logging.FileHandler(file_path().get_log_path(),
                                 encoding='utf-8')
        # 设置日志最低等级
        cl.setLevel(logging.DEBUG)
        fl.setLevel(logging.DEBUG)
        # 设置日志输出格式
        cl.setFormatter(formatter)
        fl.setFormatter(formatter)

        # 加入输出位置
        mylog.addHandler(fl)
        mylog.addHandler(cl)

        if level == 'DEBUG':
            mylog.debug(msg)
        elif level == 'INFO':
            mylog.info(msg)
        elif level == 'WARNING':
            mylog.warning(msg)
        elif level == 'ERROR':
            mylog.error(msg)
        elif level == 'CRITICAL':
            mylog.critical(msg)

        # 需要关闭日志渠道，否则每次打印会追加打印次数
        mylog.removeHandler(fl)
        mylog.removeHandler(cl)

    def debug(self, msg):
        self.my_log(msg, 'DEBUG')
    def info(self, msg):
        self.my_log(msg, 'INFO')
    def warning(self, msg):
        self.my_log(msg, 'WARNING')
    def error(self, msg):
        self.my_log(msg, 'ERROR')
    def critical(self,msg):
        self.my_log(msg,'CRITICAL')



if __name__ == '__main__':
    Mylog().debug('111')
    Mylog().warning('222')
    Mylog().warning('33')
    Mylog().error('444')
    Mylog().info('555')


import logging'''
