
from common.path_os import file_path
from common import HTMLTestRunnerNew, HTTPrequest
import unittest
from common.DoExcel import doexcel
from common.logger import Mylog
from common.DoConfig import ReadConfig

logger = Mylog()
sheetname = ReadConfig.read_config_options_list('sheetname')
caselist = doexcel().read_excel(file_path().get_case_path(), sheetname)
setattr(HTTPrequest.Gettoken, 'caselist', caselist)

def run_all():
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    from test_case import test_physicalexam_all
    suite.addTest(
        loader.loadTestsFromTestCase(test_physicalexam_all.Test_physicalexam_all))

    # 生成HTML报告
    with open(file_path().get_html_path(), 'wb') as ff:
        runner = HTMLTestRunnerNew.HTMLTestRunner(stream=ff, verbosity=2, title='Api Test Report',
                                                  description='测试报告', tester='zhaofy')

        runner.run(suite)


if __name__ == '__main__':
    run_all()
