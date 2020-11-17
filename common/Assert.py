#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author    : zhaofy
# @Datetime  : 2020/7/24 17:42
# @File      : Assert.py
# @desc      :

import json
import re
import ast
from common.logger import Mylog

log = Mylog(logger='Assert.py').getlog()


class CheckUtils:
    """检查返回数据，断言"""

    def __init__(self, check_response=None):
        self.ck_response = check_response
        self.ck_rules = {
            '无': self.no_check,
            'json键是否存在': self.check_key,
            'json键值对': self.check_keyvalue,
            '正则匹配': self.check_regexp,
            'in': self.check_str_in
        }
        self.pass_result = {
            'code': 0,
            'response_code': self.ck_response.status_code,
            'response_headers': self.ck_response.headers,
            'response_body': self.ck_response.text,
            'check_result': True,
            'message': '用例执行成功'  # 扩展作为日志输出等
        }
        self.fail_result = {
            'code': 2,
            'response_code': self.ck_response.status_code,
            'response_headers': self.ck_response.headers,
            'response_body': self.ck_response.text,
            'check_result': False,
            'message': '用例执行失败'  # 扩展作为日志输出等
        }
        self.key_list = []
        self.item_list = []

    def get_keys(self, dict_a):
        if isinstance(dict_a, dict):  # 使用isinstance检测数据类型
            # 如果为字典类型，则提取key存放到key_list中
            for x in range(len(dict_a)):
                temp_key = list(dict_a.keys())[x]
                temp_value = dict_a[temp_key]
                self.key_list.append(temp_key)
                self.get_keys(temp_value)  # 自我调用实现无限遍历
        elif isinstance(dict_a, list):
            # 如果为列表类型，则遍历列表里的元素，将字典类型的按照上面的方法提取key
            for k in dict_a:
                if isinstance(k, dict):
                    for x in range(len(k)):
                        temp_key = list(k.keys())[x]
                        temp_value = k[temp_key]
                        self.key_list.append(temp_key)
                        self.get_keys(temp_value)  # 自我调用实现无限遍历
        return self.key_list

    def get_items(self, dict_b):
        if isinstance(dict_b, dict):  # 使用isinstance检测数据类型
            # 如果为字典类型，则提取key存放到key_list中
            for x in range(len(dict_b)):
                temp_key = list(dict_b.keys())[x]
                temp_value = dict_b[temp_key]
                dict_items = {temp_key: temp_value}
                self.item_list.append(dict_items)
                self.get_items(temp_value)  # 自我调用实现无限遍历
        elif isinstance(dict_b, list):
            # 如果为列表类型，则遍历列表里的元素，将字典类型的按照上面的方法提取key
            for k in dict_b:
                if isinstance(k, dict):
                    for x in range(len(k)):
                        temp_key = list(k.keys())[x]
                        temp_value = k[temp_key]
                        dict_items = {temp_key: temp_value}
                        self.item_list.append(dict_items)
                        self.get_items(temp_value)  # 自我调用实现无限遍历
        return self.item_list

    def no_check(self, check_data=None):
        return self.pass_result

    def check_key(self, check_data=None):
        check_data_list = check_data.split(';')
        res_list = []  # 存放每次比较的结果
        wrong_key = []  # 存放比较失败key
        for c_data in check_data_list:
            if c_data in self.get_keys(self.ck_response.json()):
                res_list.append('pass')
            else:
                res_list.append('no pass')
                wrong_key.append(c_data)
        # log.info('响应中的keys有：{}'.format(self.get_keys(self.ck_response.json())))
        # log.info('期望结果是{}'.format(check_data))
        if 'no pass' in res_list:
            # log.error('用例执行失败，{}校验未通过'.format(wrong_key))
            return self.fail_result
        else:
            return self.pass_result

    def check_keyvalue(self, check_data=None):
        ck_data_list = check_data.split(';')
        res_list = []  # 存放每次比较的结果
        wrong_items = []  # 存放比较失败 items
        for ck_data in ck_data_list:
            if ast.literal_eval(ck_data) in self.get_items(self.ck_response.json()):
                res_list.append('pass')
            else:
                res_list.append('no pass')
                wrong_items.append(ck_data)
        # log.info('响应中的items有：{}'.format(self.get_items(self.ck_response.json())))
        # log.info('期望结果是{}'.format(check_data))
        if 'no pass' in res_list:
            # log.error('用例执行失败，{}校验未通过'.format(wrong_items))
            return self.fail_result
        else:
            return self.pass_result

    def check_regexp(self, check_data=None):
        pattern = re.compile(check_data)
        if re.findall(pattern=pattern, string=self.ck_response.text):
            return self.pass_result
        else:
            # log.error('用例执行失败，%s校验未通过' % check_data)
            return self.fail_result

    def check_str_in(self, check_data=None):
        """验证返回结果是否包含期望的结果"""
        log.info(self.ck_response.text)
        try:
            if check_data in self.ck_response.text:
                return self.pass_result
            else:
                return self.fail_result
        except:
            log.error("断言Fail，不包含或者body错误，body： %s,expected_body： %s" % (self.ck_response.text, check_data))
            return self.fail_result

    def assert_code(self, code, expected_code):
        """验证返回状态码相等"""
        try:
            assert int(code) == int(expected_code)
            return True
        except:
            log.error("断言Fail,code： %s,expected_code： %s" % (code, expected_code))
            raise

    def assert_body(self, body, expected_body):
        """验证返回结果内容相等"""
        try:
            assert body == expected_body
            return True
        except:
            log.error("断言Fail,body： %s,expected_body： %s" % (body, expected_body))
            raise

    def Assert_list_equal(self, list1: list, list2: list) -> bool:
        """判断两个列表的值是否完全相同"""
        list_result = []
        len1 = len(list1)
        len2 = len(list2)
        if len1 == len2:
            for i in list1:
                if i in list2 and list1.count(i) == list2.count(i):
                    list_result.append(True)
                else:
                    list_result.append(False)
            if False in list_result:
                log.error("两个列表中的值不相同")
                return False
            else:
                return True
        else:
            log.error("两个列表长度不一致")
            return False

    def isJosn(self, res):
        # 判断响应是否是json格式
        try:
            json.loads(res.text)
        except ValueError as e:
            return False
        return True

    def run_check(self, check_type=None, check_data=None):
        if check_type in self.ck_rules.keys():
            result = self.ck_rules[check_type](check_data)  # self.check_keyvalue(check_data)
            return result
        else:
            self.fail_result['message'] = '不支持%s判断方法' % check_type
            log.error('错误，%s' % self.fail_result.get('message'))
            return self.fail_result


if __name__ == '__main__':
    a = {'sheetname': 'product', 'caseid': '3', 'tag': '保存分类',
         'url': 'http://192.168.200.104:9900/api-product-admin/category',
         'method': 'post',
         'header': {'Authorization': 'Bearer 02f21152-abfd-461f-ab2f-9f3cfd4cbf2e', 'Content-Type': 'application/json'},
         'params': b'{\n  "cdesc": "\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe5\xae\xb9\xe6\x8a\xa4\xe8\x82\xa4\xe4\xb8\x8d\xe4\xba\x8c\xe4\xb9\x8b\xe9\x80\x89\xef\xbc\x8c\xe8\xbf\x98\xe4\xbd\xa0\xe5\xa4\xa9\xe4\xbd\xbf\xe5\xae\xb9\xe9\xa2\x9c\xef\xbc\x8c\xe5\x8f\x98\xe7\xbe\x8e\xe4\xb8\x8d\xe5\xae\xb9\xe9\x94\x99\xe8\xbf\x87\xef\xbc\x8c\xe5\x88\xab\xe8\xae\xa9\xe8\x87\xaa\xe5\xb7\xb1\xe5\x90\x8e\xe6\x82\x94\xe3\x80\x82\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd",\n  "chidden": 1,\n  "ckeywords": "\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8,\xe7\xbe\x8e\xe7\x99\xbd,\xe6\x8a\xa4\xe8\x82\xa4,\xe6\x8a\x97\xe8\xa1\xb0\xe8\x80\x81,\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd,\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd,\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd,\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd,\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd,\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd,\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd",\n  "clevel": "L1v\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbdo(\xe2\x88\xa9_\xe2\x88\xa9)o \xe5\x93\x88\xe5\x93\x88\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd1002020303610\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x99\xbd",\n  "cname": "\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbdo(\xe2\x88\xa9_\xe2\x88\xa9)o \xe5\x93\x88\xe5\x93\x88\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd10020",\n  "createTime": "2020-06-16T18:10:09.076Z",\n  "deleted": 0,\n  "iconUrl": "mlwl.oss-cn-shanghai.aliyuncs.com/\xe7\xba\xa2\xe5\x8c\x85\xe8\xb5\x84\xe9\x87\x91\xe6\xb5\x81\xe7\xa8\x8b\xe5\x9b\xbe.png",\n  "picUrl": "mlwl.oss-cn-shanghai.aliyuncs.com/WechatIMG41.png",\n  "id":100202036,\n  "pid": -1,\n  "sortOrder": 111,\n  "updateTime": "2020-06-15T18:10:09.076Z"\n}',
         'response': None, 'sql': None, 'expected': 'resp_code=1'}
    b = a['params']
    b = eval(b)
    print(b)
