import configparser
from common.path_os import file_path


class ReadConfig:

    @staticmethod
    def read_config(section, option):
        # 读取config文件
        cf = configparser.ConfigParser()
        cf.read(file_path().get_caseConfig_path(), encoding='utf-8')
        # 根据标签、option获取值
        res = cf.get(section, option)
        return res

    @staticmethod
    def read_config_options_value(section):
        # 读取config文件
        cf = configparser.ConfigParser()
        cf.read(file_path().get_caseConfig_path(), encoding='utf-8')
        # 根据标签获取所有options
        # options = cf.options(section)
        # 遍历获取value并放在dict
        # config_dict={}
        # for option in options:
        #     config_dict[option]=cf.get(section,option)
        rrr = cf.items(section)
        return rrr


if __name__ == '__main__':
    res = ReadConfig.read_config_options_value('MODE')
    print(res)
