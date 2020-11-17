#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author    : zhaofy
# @Datetime  : 2020/7/21 18:19
# @File      : configUtils.py
# @desc      : conf、yaml配置文件读写


import configparser
from common.path_os import file_path
from common.logger import Mylog
import yaml

log = Mylog('configUtils').getlog()


class ConfigUtils:

    def __init__(self):
        # 读取config文件
        self.cf = configparser.ConfigParser()
        self.cf.read(file_path().get_caseConfig_path(), encoding='utf-8')

    def get_config_value(self, sec, option):
        '''根据标签、option获取值'''
        res = self.cf.get(sec, option)
        return res

    def get_config_list(self, sec, section):
        """读取conf文件，处理value为list的情况"""
        # 根据标签获取所有options
        valuelist = self.get_config_value(sec, section)
        a = valuelist.lstrip('[').rstrip(']').split(',')
        print(sheets)
        print(a)
        options = self.cf.options(section)
        result = []
        for opt in options:
            rrr = self.cf.get(section, opt)
            result.append(rrr)
        return result

    def get_config_valuelist(self, section):
        '''读取conf文件，输出valuelist：[value,value,value...]'''
        # 根据标签获取所有options
        options = self.cf.options(section)
        result = []
        for opt in options:
            rrr = self.cf.get(section, opt)
            result.append(rrr)
        return result

    def get_config_dict(self, section):
        '''读取conf文件，输出dict：{key:value,key:value...}'''
        # 根据标签获取所有options
        options = self.cf.options(section)
        # 遍历获取value并放在dict
        config_dict = {}
        for option in options:
            config_dict[option] = self.cf.get(section, option)
        # rrr = cf.items(section)
        return config_dict

    def write_config(self, section, option, value):
        '''写入conf文件'''
        self.cf.set(section, option, value)  # 修改指定section 的option
        with open(file_path().get_caseConfig_path(), 'w') as f:
            self.cf.write(f)
        log.info('{} 更新成功 -> {}:{}'.format(section, option, value))


class yamlUtils:

    def __init__(self):
        self.yamlpath = file_path().get_yaml_path()

    def read(self, section=None, option=None):
        log.info('yaml中获取：{}中的{}'.format(section,option))
        with open(self.yamlpath, encoding='utf-8')as f:
            res = yaml.load(f, Loader=yaml.FullLoader)
        if section is None:
            return res
        else:
            if len(res) < 2:
                for sections, options in res.items():
                    if section not in sections:
                        return False, "未找到section"
                    elif option is None:
                        return res[section]
                    elif option not in options:
                        return False, "未找到option"
                    elif option in options:
                        return res[section][option]
            else:
                return res[section]

    def write(self, value):
        if isinstance(value, dict):
            for k, v in value.items():
                if self.read(k):
                    with open(self.yamlpath, 'a', encoding='utf-8')as f:
                        yaml.dump(value, f)
                        print("写入成功")
                else:
                    res = self.read()
                    res[k] = v
                    with open(self.yamlpath, 'a', encoding='utf-8')as f:
                        yaml.dump(res, f)
                    print("修改成功")


if __name__ == '__main__':
    # WriteConfig.write_config('Base', 'Access_Token', '33asdasdsadsadsa33')
    # a = ReadConfig.read_config_options_dict('Email')
    # print(a)
    # sheets = ConfigUtils().get_config_value('excel_case', 'SheetName')
    # a = sheets.lstrip('[').rstrip(']').split(',')
    # print(sheets)
    # print(a)
    a=yamlUtils().read('wx-token')
    print(a)