import os
import time


class file_path:
    def __init__(self):
        # 项目路径
        self.project_path = os.path.join(os.path.abspath(os.path.dirname(__file__).split('ApiAutoTest')[0]), 'ApiAutoTest')

    def get_case_path(self):
        # 用例文件路径
        case_path = os.path.join(self.project_path, 'Data',
                                 'api_test_case.xlsx')
        return case_path

    def get_html_path(self):
        # html测试报告路径
        if not os.path.exists(os.path.join(self.project_path, 'test_result')):
            os.makedirs(os.path.join(self.project_path, 'test_result'))
        html_report_path = os.path.join(self.project_path, 'test_result',
                                        str(time.strftime('%Y%m%d',
                                                          time.localtime())) + '_test_api_report.html')
        return html_report_path

    def get_caseConfig_path(self):
        # conf配置文件路径
        caseConfig_path = os.path.join(self.project_path, 'Data',
                                       'Deploy.ini')
        return caseConfig_path

    def get_log_path(self):
        # 日志文件路径
        log_path = os.path.join(self.project_path, 'log',
                                str(time.strftime('%Y%m%d', time.localtime())) + '_ApiTest.log')
        return log_path

    def get_yaml_path(self):
        # yaml配置文件路径
        yaml_path = os.path.join(self.project_path, 'Data', 'Base_data.yaml')
        return yaml_path

    def get_demo_conf(self):
        caseConfig_path = os.path.join(self.project_path, 'Data',
                                       'demo.ini')
        return caseConfig_path


if __name__ == '__main__':
    import time

    # print(os.path.join(os.path.split(os.getcwd())[0],'log',str(time.strftime('%Y%m%d',time.localtime()))+'_ApiTest.log'))
    a=file_path().get_caseConfig_path()
    print(a)
    # print(type(time.strftime('%Y%m%d',time.localtime())))
