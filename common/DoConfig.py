import configparser
from common.path_os import file_path
from common.logger import Mylog
log =Mylog()

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

    @staticmethod
    def read_config_options_list(section):
        cf = configparser.ConfigParser()
        cf.read(file_path().get_caseConfig_path(), encoding='utf-8')
        opt_list = cf.options(section)
        result = []
        for opt in opt_list:
            rrr = cf.get(section, opt)
            result.append(rrr)
        return result


class WriteConfig:
    @staticmethod
    def write_config(section, option, value):
        cf = configparser.ConfigParser()
        cf.read(file_path().get_caseConfig_path(), encoding='utf-8')
        cf.add_section(section)
        cf.set(section, option, value)  # 修改指定section 的option
        with open(file_path().get_caseConfig_path(),'w') as f:
            cf.write(f)
        log.info('{} 更新成功'.format(section))


if __name__ == '__main__':
    WriteConfig.write_config('mysql', 'host', '199.199.199.199')

