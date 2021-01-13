#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author    : zhaofy
# @Datetime  : 2020/7/24 17:42
# @File      : TestHttpRequest.py
# @desc      :

import unittest, urllib3
from ddt import ddt, data
from common.requestUtils import RequestUtils
from common.dataUtils import *
import datetime, time
from common.configUtils import *

logger = Mylog('TestHttpRequest.py').getlog()
# 读取deploy.ini文件excel_case（执行哪些sheet）
sheets = eval(ConfigUtils().get_config_value('excel_case', 'SheetName'))
# 读取api_test_case.xlsx文件返回测试用例集
caseinfos = DataUtils(sheets).testCaseDataList()


@ddt
class Test_Http_Request(unittest.TestCase):

    def setUp(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.start_time = datetime.datetime.now()

    def tearDown(self):
        end_time = datetime.datetime.now()
        logger.info('耗时：{}'.format(end_time - self.start_time))
        time.sleep(0.5)

    @data(*caseinfos)
    def test_api(self, caselist):
        """用例名称：{}""".format(caselist.get("测试用例名称"))
        log.info("测试用例[ %s ]开始执行" % (str(caselist.get("测试用例编号")) + caselist.get("测试用例名称")))
        self._testMethodName = caselist.get('测试用例编号')
        self._testMethodDoc = caselist.get('测试用例名称')
        results = RequestUtils().request_by_step(caselist)
        for result in results:
            try:
                self.assertTrue(result.get('check_result'), True)
                logger.info(
                    "用例 %s:%s 执行成功[%s]" % (caselist.get("测试用例编号"), caselist.get("测试用例名称"), result.get('message')))
            except AssertionError as e:
                logger.error(
                    "用例 %s:%s 执行失败[%s]" % (caselist.get("测试用例编号"), caselist.get("测试用例名称"), result.get('message')))


if __name__ == '__main__':
    unittest.main()
