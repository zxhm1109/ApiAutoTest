import unittest, requests
from ddt import ddt, data
from common.HTTPrequest import Gettoken
from common import HTTPrequest, DoExcel
from common.path_os import file_path
from common.logger import Mylog

log=Mylog()
sheetname = 'physicalexam'
caselist = DoExcel.doexcel().read_excel(file_path().get_case_path(), sheetname)


@ddt
class TestHttpRequest(unittest.TestCase):
    def setUp(self):
        log.info('---------------开始执行用例-------------------')
        # 去除异常提示
        requests.packages.urllib3.disable_warnings()


    @data(*caselist)
    def test_api(self, caselist):
        log.info('test_api')
        res = HTTPrequest.http_request.httprequest(caselist['url'],
                                                   caselist['params'],
                                                   caselist['method'],
                                                   getattr(Gettoken, 'TOKEN'))
        try:
            self.assertIn(caselist['expected'], res.json()['message'])
            Testresult = 'Pass'
        except AssertionError as e:
            Testresult = 'Fail'
            print('用例执行出错：{}'.format(e))
            raise e
        finally:
            # 执行结果写入case文件
            DoExcel.doexcel().write_excel(file_path().get_case_path(),
                                          sheetname,
                                          int(caselist['caseid']) + 1,
                                          Testresult)


# def test_api111(self):
#     a = 1
#     b = 2
#     c=False
#     if self.assertEqual(3, a + b):
#         c=True
#     print(c)

def tearDown(self):
    log.info('-------------用例执行结束-----------------')


TestHttpRequest()
