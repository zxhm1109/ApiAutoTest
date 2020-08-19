import logging
from common.path_os import file_path
import os, datetime, time


class Mylog(logging.Logger):

    def __init__(self,
                 name="root",
                 level="DEBUG",
                 format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s-> %(message)s'
                 ):
        # logger(name) 直接超继承logger当中的name
        super().__init__(name)

        # 设置收集器级别
        # logger.setLevel(level)
        self.setLevel(level)  # 继承了Logger 返回的实例就是自己

        # 初始化format，设置格式
        fmt = logging.Formatter(format)

        # 初始化处理器
        # 如果file为空，就执行stream_handler,如果有，两个都执行

        file_handler = logging.FileHandler(file_path().get_log_path(), encoding='utf-8')
        # 设置handler级别
        file_handler.setLevel(level)
        # 添加handler
        self.addHandler(file_handler)
        # 添加日志处理器
        file_handler.setFormatter(fmt)

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(level)
        self.addHandler(stream_handler)
        stream_handler.setFormatter(fmt)


def del_overdue_log_file(filepath):
    nowtime = time.strftime('%Y%m%d')
    logger = Mylog()
    # 遍历文件夹下文件列表
    for x, y, z in os.walk(filepath):
        for i in z:
            filetime = i.split('_')[0]

            # 当前月份大于文件月份2个月及2个月以上时，清理文件
            if (int(nowtime[4:6]) - int(filetime[4:6])) > 1:
                os.remove(os.path.join(filepath, i))
                logger.info('清理历史文件成功！')
            # 当前月份大于文件月份1个月 且 当前日大于文件日时，清理文件
            elif int(filetime[6:]) < int(nowtime[6:]) and (int(nowtime[4:6]) - int(filetime[4:6])) == 1:
                os.remove(os.path.join(filepath, i))
                logger.info('清理历史文件成功！')
            else:
                pass


def del_log_report():
    log_file_path = os.path.join(os.path.abspath(os.path.dirname(__file__).split('ApiAutoTest')[0]), 'ApiAutoTest\log\\')
    # 测试报告文件夹路径
    report_file_path = os.path.join(os.path.abspath(os.path.dirname(__file__).split('ApiAutoTest')[0]), 'ApiAutoTest\\test_result\\')
    del_overdue_log_file(log_file_path)
    del_overdue_log_file(report_file_path)


if __name__ == '__main__':
    logger = Mylog()
    logger.debug("world")
    # 日志文件夹路径
    log_file_path = os.path.join(os.path.abspath(os.path.dirname(__file__).split('ApiAutoTest')[0]), 'ApiAutoTest\log\\')
    # 测试报告文件夹路径
    report_file_path = os.path.join(os.path.abspath(os.path.dirname(__file__).split('ApiAutoTest')[0]), 'ApiAutoTest\\test_report\\')
    del_overdue_log_file(report_file_path)
