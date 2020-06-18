import unittest
from ddt import ddt, data
from common.HTTPrequest import Gettoken
from common import HTTPrequest, DoExcel
from common.path_os import file_path
from common.logger import Mylog
import datetime
from common.DoConfig import ReadConfig

log = Mylog()

caselist = getattr(Gettoken, 'caselist')
log.info(caselist)
Testresult = 'Invalid Assert'


@ddt
class Test_physicalexam_all(unittest.TestCase):

    def setUp(self):

        log.info('---------------开始执行用例-------------------')
        self.start_time = datetime.datetime.now()

    def tearDown(self):
        log.info('---------------用例执行结束-------------------')
        end_time = datetime.datetime.now()
        log.info('耗时：{}'.format(end_time - self.start_time))

    @data(*caselist)
    def test_api(self, caselist):
        if not caselist['header']:
            res = HTTPrequest.http_request.httprequest(caselist['url'],
                                                       caselist['params'],
                                                       caselist['method'],
                                                       token=ReadConfig.read_config('Access_Token',
                                                                                    'token'))
        else:
            res = HTTPrequest.http_request.httprequest(caselist['url'],
                                                       caselist['params'],
                                                       caselist['method'],
                                                       header=caselist['header'],
                                                       token=ReadConfig.read_config('Access_Token',
                                                                                    'token'))
        try:
            self.assertEqual(caselist['expected'], str(res['resp_code']))
            Testresult = 'Pass'
        except AssertionError as e:
            Testresult = 'Fail'
            log.error('用例执行出错：{}'.format(e))
            raise e
        finally:
            # 执行结果写入case文件
            DoExcel.doexcel().write_excel(file_path().get_case_path(),
                                          caselist['sheetname'],
                                          int(caselist['caseid']) + 1,
                                          Testresult)
