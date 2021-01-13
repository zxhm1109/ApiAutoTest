#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author    : zhaofy
# @Datetime  : 2020/7/24 17:42
# @File      : Run.py
# @desc      :

import unittest
from common.logger import Mylog
from common.To_Emil import ToEmail
from common.path_os import file_path
import os, time
from common import HTMLTestReportCN

logger = Mylog('run.py').getlog()


class Run:

    def __init__(self):
        self.log_file_path = os.path.join(os.path.abspath(os.path.dirname(__file__).split('ApiAutoTest')[0]),
                                          'ApiAutoTest\log\\')
        # 测试报告文件夹路径
        self.report_file_path = os.path.join(os.path.abspath(os.path.dirname(__file__).split('ApiAutoTest')[0]),
                                             'ApiAutoTest\\report\\')
        self.case_path = file_path().get_case_py_path()
        self.report_path = file_path().get_report_html_path()
        self.title = '自动化测试报告'
        self.describe = 'SSBM项目接口自动化测试报告'
        self.tester = 'zhaofy'

    def del_overdue_file(self, filepath):
        # 清理文件夹内一月前的文件
        nowtime = time.strftime('%Y%m%d')
        # 遍历文件夹下文件列表
        for x, y, z in os.walk(filepath):
            for i in z:
                filetime = i.split('_')[0]
                # 当前月份大于文件月份2个月及2个月以上时，清理文件
                if (int(nowtime[4:6]) - int(filetime[4:6])) > 1:
                    os.remove(os.path.join(filepath, i))
                    logger.info('清理历史文件成功！')
                # 当前月份大于文件月份1个月 且 当前日大于文件日时，清理文件
                elif int(filetime[6:]) < int(nowtime[6:]) and (int(nowtime[4:6]) - int(filetime[4:6])) == 1:
                    os.remove(os.path.join(filepath, i))
                    logger.info('清理历史文件成功！')
                else:
                    pass

    def load_testsuite(self):
        discover = unittest.defaultTestLoader.discover(
            start_dir=self.case_path,
            pattern='TestHttpRequest.py',
            top_level_dir=self.case_path
        )
        all_suite = unittest.TestSuite()
        all_suite.addTest(discover)
        return all_suite

    def run(self):
        # 清理 一个月前的日志和测试报告
        self.del_overdue_file(self.log_file_path)
        self.del_overdue_file(self.report_file_path)

        # 生成HTML报告
        fp = open(self.report_path, 'wb')
        runner = HTMLTestReportCN.HTMLTestRunner(
            stream=fp,
            title=self.title,
            description=self.describe,
            tester=self.tester
        )
        runner.run(self.load_testsuite())
        fp.close()

        # 生成测试报告并发送至邮箱
        # with open(self.report_path, 'rb') as f:
        #     mail_boby = f.read()
        # ToEmail().sendemail(mail_boby)
        # logger.info('HTML测试报告地址：{}'.format(self.report_path))


# def run_all():
#     suite = unittest.TestSuite()
#     loader = unittest.TestLoader()
#     from test_case import TestHttpRequest
#     suite.addTest(
#         loader.loadTestsFromTestCase(TestHttpRequest.Test_Http_Request))
#     # 生成HTML报告
#     with open(file_path().get_report_html_path(), 'wb') as ff:
#         runner = HTMLTestRunnerNew.HTMLTestRunner(stream=ff, verbosity=1, title='Api Test Report',
#                                                   description='测试报告', tester='zhaofy')
#         runner.run(suite)
#
#     #发送测试报告至邮箱
#     with open(file_path().get_report_html_path(), 'rb') as f:
#         mail_boby = f.read()
#     ToEmail(mail_boby)


if __name__ == '__main__':
    Run().run()
