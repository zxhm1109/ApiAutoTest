from common.path_os import file_path
from common import HTMLTestRunnerNew, HTTPrequest
import unittest
from common.DoExcel import *
from common.logger import *
from common.DoConfig import ReadConfig
from common.To_Emil import ToEmail

logger = Mylog()
sheetname = ReadConfig.read_config_options_dict('excel_case')
caselist = get_case_data(sheetname)


def run_all():
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    from test_case import TestHttpRequest
    suite.addTest(
        loader.loadTestsFromTestCase(TestHttpRequest.Test_Http_Request))
    # 生成HTML报告
    with open(file_path().get_html_path(), 'wb') as ff:
        runner = HTMLTestRunnerNew.HTMLTestRunner(stream=ff, verbosity=1, title='Api Test Report',
                                                  description='测试报告', tester='zhaofy')
        runner.run(suite)

    #发送测试报告至邮箱
    with open(file_path().get_html_path(), 'rb') as f:
        mail_boby = f.read()
    ToEmail(mail_boby)


if __name__ == '__main__':
    # 清理历史文件
    del_log_report()
    run_all()
