from openpyxl import load_workbook
import json
from common.read_config import ReadConfig
from common.Loggin import Mylog

log=Mylog()
res=ReadConfig.read_config_options_value('MODE')

class doexcel:

    @staticmethod
    def read_excel(filepath, sheetname):
        log.info('读取用例')
        wb = load_workbook(filepath)
        sheet = wb[sheetname]
        test_case = []

        for i in range(2, sheet.max_row + 1):
            row_data = {}
            row_data['caseid'] = sheet.cell(i, 1).value
            row_data['url'] = sheet.cell(i, 5).value
            row_data['method'] = sheet.cell(i, 6).value
            row_data['params'] = sheet.cell(i, 8).value
            row_data['tag'] = sheet.cell(i, 3).value
            row_data['expected'] = sheet.cell(i, 9).value
            test_case.append(row_data)
        return test_case

    def write_excel(self, filepath, sheetname, row, value=None):
        # 读取文件
        wb = load_workbook(filepath)
        # 打开excel表单
        sheet = wb[sheetname]
        # 对应行列写入数据
        sheet.cell(row, 10).value = value
        # 保存文件
        wb.save(filepath)


def load_params(params):
    if len(params) > 0:
        return json.dumps(json.loads(params))

    else:
        return params


if __name__ == '__main__':
    from common.path_os import file_path

    sheetname = 'physicalexam'
    # a = doexcel.read_excel(file_path().get_case_path(), sheetname)
    # print(a)
