# import logging
from common.path_os import file_path
#
#
# class Mylog:
#
#     def my_log(self, msg, level):
#         # 创建logger实例
#         mylog = logging.getLogger('__main__')
#         #设置日志等级
#         mylog.setLevel(logging.DEBUG)
#
#         # 定义日志输入格式
#         formatter = logging.Formatter(
#             '%(asctime)s %(filename)s->line:%(lineno)d %(levelname)s: %(message)s')
#
#         # 设置日志输出位置
#         cl = logging.StreamHandler()
#         fl = logging.FileHandler(file_path().get_log_path(),
#                                  encoding='utf-8')
#         # 设置日志最低等级
#         cl.setLevel(logging.DEBUG)
#         fl.setLevel(logging.DEBUG)
#         # 设置日志输出格式
#         cl.setFormatter(formatter)
#         fl.setFormatter(formatter)
#
#         # 加入输出位置
#         mylog.addHandler(fl)
#         mylog.addHandler(cl)
#
#         if level == 'DEBUG':
#             mylog.debug(msg)
#         elif level == 'INFO':
#             mylog.info(msg)
#         elif level == 'WARNING':
#             mylog.warning(msg)
#         elif level == 'ERROR':
#             mylog.error(msg)
#         elif level == 'CRITICAL':
#             mylog.critical(msg)
#
#         # 需要关闭日志渠道，否则每次打印会追加打印次数
#         mylog.removeHandler(fl)
#         mylog.removeHandler(cl)
#
#     def debug(self, msg):
#         self.my_log(msg, 'DEBUG')
#     def info(self, msg):
#         self.my_log(msg, 'INFO')
#     def warning(self, msg):
#         self.my_log(msg, 'WARNING')
#     def error(self, msg):
#         self.my_log(msg, 'ERROR')
#     def critical(self,msg):
#         self.my_log(msg,'CRITICAL')
#
#
#
# if __name__ == '__main__':
#     Mylog().debug('111')
#     Mylog().warning('222')
#     Mylog().warning('33')
#     Mylog().error('444')
#     Mylog().info('555')


import logging


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

        file_handler = logging.FileHandler(file_path().get_log_path(),encoding='utf-8')
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


logger = Mylog()

if __name__ == '__main__':
    logger = Mylog()
    logger.debug("world")
