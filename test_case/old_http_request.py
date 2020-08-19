import unittest, requests
from ddt import ddt, data
from common.HTTPrequest import Gettoken
from common import HTTPrequest, DoExcel
from common.path_os import file_path
from common.logger import Mylog
from common.DoConfig import ReadConfig

logger = Mylog()
sheetname = ReadConfig.read_config_options_list('sheetname')
caselist = DoExcel.doexcel().read_excel(sheetname)
Testresult = 'Invalid Assert'


@ddt
class TestHttpRequest(unittest.TestCase):
    def setUp(self):
        logger.info('---------------开始执行用例-------------------')
        # 去除https证书提示
        requests.packages.urllib3.disable_warnings()

    def tearDown(self):
        logger.info('-------------用例执行结束-----------------')

    @data(*caselist)
    def test_api(self, caselist):
        res = HTTPrequest.http_request.httprequest(caselist['url'],
                                                   caselist['params'],
                                                   caselist['method'],
                                                   ReadConfig.read_config('Base', 'access_token'))
        try:
            self.assertIn(caselist['expected'], res.json()['message'])
            Testresult = 'Pass'
        except AssertionError as e:
            Testresult = 'Fail'
            logger.error('用例执行出错：{}'.format(e))
            raise e
        finally:
            # 执行结果写入case文件
            DoExcel.doexcel().write_excel(sheetname=sheetname,row=int(caselist['caseid']) + 1,value=Testresult)


if __name__ == '__main__':
    unittest.main()
