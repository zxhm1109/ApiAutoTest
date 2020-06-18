from openpyxl import load_workbook
import json
from common.DoConfig import ReadConfig
from common.logger import Mylog

log=Mylog()
res=ReadConfig.read_config_options_value('MODE')
host = ReadConfig.read_config('HOST', 'host')


class doexcel:

    @staticmethod
    def read_excel(filepath, sheetname):
        log.info('读取用例')
        wb = load_workbook(filepath)
        test_case = []
        for sheet1 in sheetname:

            sheet = wb[sheet1]

            for i in range(2, sheet.max_row + 1):
                if sheet.cell(i,2).value.lower() == 'y':
                    row_data = {}
                    row_data['caseid'] = sheet.cell(i, 1).value
                    row_data['sheetname'] = sheet1
                    row_data['url'] = host + str(sheet.cell(i, 5).value)
                    row_data['tag'] = sheet.cell(i, 3).value
                    row_data['expected'] = sheet.cell(i, 9).value
                    row_data['method'] = sheet.cell(i, 6).value

                    if sheet.cell(i, 7).value == 'application/json':
                        row_data['header'] = sheet.cell(i, 7).value
                        parms = sheet.cell(i, 8).value
                        row_data['params'] = json.dumps(eval(parms))
                    elif sheet.cell(i, 7).value is None:
                        row_data['params'] = ''
                        row_data['header'] = ''
                    else:
                        row_data['params'] = sheet.cell(i, 8).value
                        row_data['header'] =sheet.cell(i,7).value

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
        try:
            wb.save(filepath)
        except PermissionError as e:
            log.error('用例执行结果写入失败，如已打开请关闭！')


def load_params(params):
    if len(params) > 0:
        return json.dumps(json.loads(params))

    else:
        return params


if __name__ == '__main__':
    sheetname = 'physicalexam'
    # a = doexcel.read_excel(file_path().get_case_path(), sheetname)
    # print(a)
