#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author    : zhaofy
# @Datetime  : 2020/11/9 14:10 
# @File      : DataUtils.py 
# @desc      : 测试数据处理

from common.logger import Mylog
from common.excelUtils import ExcelUtils

logger = Mylog('dataUtils.py').getlog()


class DataUtils:
    """处理excel表格测试用例符合Test_Http_Request 数据格式 """

    def __init__(self, sheet_name):
        self.sheet_names = sheet_name

    # def getTestCaseData(self):
    #     testCaseDict = {}
    #     for row_data in self.testData:
    #         testCaseDict.setdefault(row_data['测试用例编号'], []).append(row_data)
    #     return testCaseDict

    def testCaseDataList(self):

        testCaseList = []
        for sheet_name in self.sheet_names:
            testData = ExcelUtils(sheet_name).ReadExcel()
            for row_data in testData:
                if int(row_data.get("是否执行")):
                    testCaseList.append(row_data)
        logger.info('待执行测试用例集：' + str(testCaseList))
        return tuple(testCaseList)


class transfer_data:
    temporary_variables = {}


if __name__ == "__main__":
    from common.configUtils import ConfigUtils

    sheets = eval(ConfigUtils().get_config_value('excel_case', 'SheetName'))
    for sheet in sheets:
        a = DataUtils(sheet).testCaseDataList()
        print(a)
