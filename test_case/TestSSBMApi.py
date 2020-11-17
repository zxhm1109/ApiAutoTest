#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author    : zhaofy
# @Datetime  : 2020/11/17 15:48
# @File      : TestSSBMApi.py
# @desc      :

import unittest
import warnings
from common.requestUtils import RequestUtils
from common.logger import Mylog
import paramunittest
from common.dataUtils import DataUtils
from common.configUtils import ConfigUtils

# 初始化一个日志对象
log = Mylog(logger='TestSSBMApi').getlog()

# 读取deploy.ini文件excel_case（执行哪些sheet）
sheets = ConfigUtils().get_config_value('excel_case', 'SheetName')
# 读取api_test_case.xlsx文件返回测试用例集
case_infos = DataUtils(sheets).testCaseDataList()


@paramunittest.parametrized(
    *case_infos
)
class Test_SSBM_Api(paramunittest.ParametrizedTestCase):
    def setUp(self):
        warnings.simplefilter('ignore', ResourceWarning)

    def setParameters(self, case_id, case_info):
        self.case_id = case_id
        self.case_info = case_info

    def test_base_run(self):
        log.info("测试用例[ %s ]开始执行" % (str(self.case_info[0].get("测试用例编号")) + self.case_info[0].get("测试用例名称")))
        self._testMethodName = self.case_info[0].get('编号')
        self._testMethodDoc = self.case_info[0].get('用例名称')
        results = RequestUtils().request_by_step(self.case_info)
        log.info('results:{}'.format(results))
        for result in results:
            self.assertTrue(result.get('check_result'), result.get('message'))


if __name__ == '__main__':
    unittest.main()
