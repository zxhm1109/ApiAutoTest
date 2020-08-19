import unittest ,urllib3
from ddt import ddt, data
from common.DoYaml import DoYaml
from common import HTTPrequest, DoExcel
from common.logger import *
import datetime
from common.DoConfig import *
from common.Assert import Assert
from common.redis_connect import get_img_code
from common.mysql_connect import mysql

logger = Mylog()
DoExcel.get_excel_base_wite_conf()
sheetname = ReadConfig.read_config_options_dict('excel_case')
caselist = DoExcel.get_case_data(sheetname)
logger.info('获取excel测试用例：{}'.format(caselist))


@ddt
class Test_Http_Request(unittest.TestCase):

    def setUp(self):

        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.start_time = datetime.datetime.now()

    def tearDown(self):
        end_time = datetime.datetime.now()
        logger.info('耗时：{}  \n'.format(end_time - self.start_time))
        time.sleep(0.5)

    @data(*caselist)
    def test_api(self, caselist):

        res = HTTPrequest.http_request.HttpReqest(caselist)
        rw_demo_conf().w_demo('key', caselist['caseid'], caselist['tag'])
        rw_demo_conf().w_demo('value', caselist['caseid'], str(res.text)[:200])
        logger.info('返参：{},HTTPSTUTAS:{}'.format(res.text,res.status_code))
        if caselist['response']:
            if caselist['response'] == 'imgcode':
                get_img_code('DEFAULT_CODE_KEY:' + ReadConfig.read_config('Base', 'deviceid'))
        elif caselist['response'] and res['datas']:
            WriteConfig.write_config('Base', caselist['response'], res.json()['data'][caselist['response']])
        if caselist['sql']:
            DB = DoYaml().read(section='database')
            sql_res = mysql.connect_mysql(DB[caselist['sheetname']], caselist['sql'])
            logger.info('sql:{}'.format(sql_res))
        Testresult = 'Fail'
        x, j, k, l = Assert(caselist['expected'], res)
        if x:
            Testresult = 'Pass'
            logger.info('断言SUCCEED --> {}：{} == {}'.format(j, k, l))
        else:
            logger.error('断言FAILURE --> {}: {} != {}'.format(j, k, l))
            raise AssertionError('{} != {}'.format(k, l))
        DoExcel.doexcel().write_excel(caselist['sheetname'],
                                      int(caselist['caseid'].split('_')[-1]) + 1,
                                      Testresult)


if __name__ == '__main__':
    unittest.main()
