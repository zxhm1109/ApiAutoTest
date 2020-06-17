from common import test_http_request
import unittest


def run():
    # path = r'D:\PyPackage\test_file\api_test_case.xlsx'
    # sheetname = 'physicalexam'
    # restult=DoExcel.load_params(path,sheetname)

    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    suite.addTest(
        loader.loadTestsFromTestCase(test_http_request.TestHttpRequest))

    suite.run()

    # 生成HTML报告
    # with open(file_path().get_html_path(),'wb') as file:
    #
    #     pass

run()