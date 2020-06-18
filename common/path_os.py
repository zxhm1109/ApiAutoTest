import os
import time


class file_path:
    def __init__(self):
        self.project_path = \
            os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]

    def get_case_path(self):
        case_path = os.path.join(self.project_path, 'Data',
                                 'api_test_case.xlsx')
        return case_path

    def get_html_path(self):
        if not os.path.exists(os.path.join(self.project_path, 'test_result')):
            os.makedirs(os.path.join(self.project_path, 'test_result'))
        html_report_path = os.path.join(self.project_path, 'test_result',
                                        str(time.strftime('%Y%m%d',
                                                          time.localtime())) + '_test_api_report.html')
        return html_report_path

    def get_caseConfig_path(self):
        caseConfig_path = os.path.join(self.project_path, 'Data',
                                       'Deploy.config')
        return caseConfig_path

    def get_log_path(self):

        log_path = os.path.join(self.project_path, 'log',
                                str(time.strftime('%Y%m%d', time.localtime())) + '_ApiTest.log')
        return log_path


if __name__ == '__main__':
    # for path,filder,file in os.walk(os.path.join(os.path.split(os.getcwd())[0],'common')):
    #     print(file)
    import time

    # print(os.path.join(os.path.split(os.getcwd())[0],'log',str(time.strftime('%Y%m%d',time.localtime()))+'_ApiTest.log'))
    file_path().get_log_path()

    # print(type(time.strftime('%Y%m%d',time.localtime())))
