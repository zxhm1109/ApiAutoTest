#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author    : zhaofy
# @Datetime  : 2020/11/9 14:10
# @File      : HTTPrequest.py
# @desc      : http请求封装
"""
变量入参处理
非json格式响应处理
1.依据excel用例中的请求方式完成不同的请求
2.请求头的处理（不同的请求的请求头不同，是否需要写在excel的用例中？）：
    i.accept、accept-encoding、Content-Type、user-agent是固定的(是否需要根据端的不同进行更改)
    ii.ex-token是调用登录接口后获取响应中的token
3.响应的处理：
    i.通过正则表达式或者jsonpath获取响应中的某些值，可作为下一个接口的入参
    ii.key放在excel中，通过key取对应的value
    iii.响应参数非json格式时的处理
4.断言
    i.响应信息中需要的业务参数的key存放再excel中，作为执行结果
    ii.期望的值填写再excel中，作为期望结果
"""

import ast  # ast.literal_eval 与eval()功能相似，但更安全
import time
from common.Assert import CheckUtils
import jsonpath
import requests
import json, re
from requests.exceptions import RequestException
from common.configUtils import ConfigUtils
from common.dataUtils import transfer_data
from common.logger import Mylog

# 去除异常提示 https ssl
# import urllib3
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

log = Mylog('requestUtils.py').getlog()


class RequestUtils:
    """处理request请求及响应数据"""

    def __init__(self):
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1 wechatdevtools/1.02.1911180 MicroMessenger/7.0.4 Language/zh_CN webview/"
        }
        # self.temporary_variables = {}

    def temporary_variables(self, rw, kw):
        if rw == 'w':
            setattr(transfer_data, 'temporary_variables', kw)
        else:
            getattr(transfer_data, 'temporary_variables')

    def headerUtils(self, case_info):
        '''判断是否需要补充请求头信息'''
        if case_info['是否补充请求头']:
            log.info('11中转数据temporary_variables：{}'.format(self.temporary_variables('r', 'wx-token')))
            self.headers['wx-token'] = self.temporary_variables('r', 'wx-token')
            log.info('请求头信息更新，目前请求头信息为：%s' % self.headers)
        else:
            log.info('请求头信息保持不变，目前请求头信息为：%s' % self.headers)
            pass

    def processRequestData(self, case_info):
        """处理请求参数问题：参数化、参数化格式"""
        # 替换url中的变量
        url__variable_list = re.findall('\\${\w+}', case_info['请求地址'])
        if url__variable_list:
            case_info['请求地址'] = case_info['请求地址'].replace(url__variable_list, self.temporary_variables('r', url__variable_list[2:-1]))
            log.info("将%s替换为%s，替换请求地址成功！" % (url__variable_list, self.temporary_variables('r', url__variable_list[2:-1])))
        # 替换请求参数(get)中的变量
        postParam_variable_list = re.findall('\\${\w+}', case_info['请求参数'])
        if postParam_variable_list:
            case_info['请求参数'] = case_info['请求参数'].replace(postParam_variable_list, self.temporary_variables('r', postParam_variable_list[2:-1]))
            log.info("将%s替换为%s，替换请求参数成功！" % (postParam_variable_list, self.temporary_variables('r', postParam_variable_list[2:-1])))
        # 替换取值代码中的变量
        code_variable_list = re.findall('\\${\w+}', case_info['取值变量'])
        if code_variable_list:
            case_info['取值代码'] = case_info['取值代码'].replace(code_variable_list, self.temporary_variables('r', code_variable_list[2:-1]))
            log.info("将%s替换为%s，替换取值代码成功！" % (code_variable_list, self.temporary_variables('r', code_variable_list[2:-1])))
        # 替换期望结果中的变量
        result_variable_list = re.findall('\\${\w+}', case_info['期望结果'])
        if result_variable_list:
            case_info['期望结果'] = case_info['期望结果'].replace(result_variable_list, self.temporary_variables('r', result_variable_list[2:-1]))
            log.info("将%s替换为%s，替换期望结果成功！" % (result_variable_list, self.temporary_variables('r', result_variable_list[2:-1])))

    def processResponseData(self, case_info, res):
        '''处理响应数据（提取数据参数化）'''
        if case_info["取值变量"]:
            try:
                log.info("取值：{},{}".format(case_info["取值变量"], res))
                get_value_code_list = case_info["取值变量"].split(";")
                dic = {}
                for ii in range(0, len(get_value_code_list)):
                    iii = get_value_code_list[ii].split("=")
                    value = jsonpath.jsonpath(res.json(), iii[1])[-1]
                    dic[iii[0]] = str(value)
                    self.temporary_variables('w', dic)
                    log.info("取值：{},{}".format(self.temporary_variables('r', "wx-token"), res))
            except Exception as e:
                log.error("发生错误，%s" % e)
        # elif case_info["取值方式"] == "正则取值":
        #     try:
        #         get_value_code_list = case_info["取值代码"].split(";")
        #         log.info('get_value_code_list = %s' % get_value_code_list)
        #         transfer_value_variable_list = case_info["传值变量"].split(";")
        #         log.info('transfer_value_variable_list = %s' % transfer_value_variable_list)
        #         for i in range(0, len(get_value_code_list)):
        #             # log.info('i = %d' % i)
        #             log.info("取值代码为：%s" % get_value_code_list[i])
        #             try:
        #                 value = re.findall(get_value_code_list[i], res.text)[-1]
        #                 log.info('value = %s' % value)
        #                 self.temporary_variables[transfer_value_variable_list[i]] = value
        #             except IndexError as e:
        #                 log.error("无法依据正则表达式匹配到值")
        #     except Exception as e:
        #         log.error("发生错误，%s" % e)
        else:
            pass

    def sendrequest(self, case_info):
        self._addTimeStampToTemp()
        self.processRequestData(case_info)
        log.info("取值代码为：%s" % case_info['取值变量'])
        url = ConfigUtils().get_config_value('Base', 'host') + case_info['请求地址']
        self.headerUtils(case_info)
        log.info('请求方式为：%s\n请求地址为：%s?%s\n请求参数为：%s' % (
            case_info['请求方式'], url, case_info['请求参数'], case_info['请求参数']))
        try:
            if case_info["请求方式"].upper() == "GET":
                geturl = url + '?' + case_info['请求参数']
                res = requests.get(
                    url=geturl,
                    headers=self.headers
                )
                res.encoding = res.apparent_encoding
                log.info('响应状态码为：%s\n响应信息为：%s' % (res.status_code, res.text))
                return res
            elif case_info["请求方式"].upper() == "POST":
                if case_info['请求参数'] == '':
                    res = requests.post(
                        url=url,
                        headers=self.headers
                    )
                    res.encoding = res.apparent_encoding
                    log.info('响应状态码为：%s\n响应信息为：%s' % (res.status_code, res.text))
                    return res
                else:
                    res = requests.post(
                        url=url,
                        headers=self.headers,
                        data=ast.literal_eval(case_info['请求参数'])
                    )
                    res.encoding = res.apparent_encoding
                    log.info('响应状态码为：%s\n响应信息为：%s' % (res.status_code, res.text))
                    return res
            elif case_info["请求方式"].upper() == "PUT":
                res = requests.put(
                    url=url,
                    headers=self.headers,
                    data=case_info['请求参数'],
                    json=ast.literal_eval(case_info['请求参数'])
                )
                res.encoding = res.apparent_encoding
                log.info('响应状态码为：%s\n响应信息为：%s' % (res.status_code, res.text))
                return res
            elif case_info["请求方式"].upper() == "DELETE":
                geturl = url + '?' + case_info['请求参数']
                res = requests.delete(
                    url=geturl,
                    headers=self.headers
                )
                res.encoding = res.apparent_encoding
                log.info('响应状态码为：%s\n响应信息为：%s' % (res.status_code, res.text))
                return res
        except ConnectionError as e:
            log.error('[%s]请求：连接超时异常' % (case_info["请求地址"]), e.__str__())
        except RequestException as e:
            log.error('[%s]请求：Request异常，原因：%s' % (case_info["请求地址"], e.__str__()))
        except Exception as e:
            log.error('[%s]请求：系统异常，原因：%s' % (case_info["请求地址"], e.__str__()))

    def _addTimeStampToTemp(self):
        timestamp = int(time.time())
        self.temporary_variables('w', {'timestamp': str(timestamp)})

    def checkreuqst(self, case_info):
        log.info("case_info:{}".format(case_info))
        log.info("开始执行步骤%s：%s" % (case_info['测试用例编号'], case_info['测试用例名称']))
        res = self.sendrequest(case_info)
        self.processResponseData(case_info, res)
        # log.info('此时变量有：%s' % self.temporary_variables)
        result = CheckUtils(res).run_check(case_info['期望结果类型'], case_info['期望结果'])
        if not result.get('check_result'):
            log.error("步骤\"%s:%s\"执行失败" % (case_info['测试用例编号'], case_info['测试用例名称']))
        return result

    def request_by_step(self, case_infos):
        temp_result_list = []
        # for case_info in case_infos:
        temp_result = self.checkreuqst(case_infos)
        temp_result_list.append(temp_result)
        return temp_result_list


if __name__ == '__main__':
    # data = {'sheetname': 'login', 'caseid': 'login_1', 'tag': '账号密码登录',
    #         'url': 'https://t2wxapi.sancell.top//ssxq/w/auth/pin',
    #         'method': 'post', 'header': {'Content-Type': 'application/json;charset=UTF-8',
    #                                      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'},
    #         'params': '{"phone": "17621757807","pin_type": "login"}',
    #         'response': None, 'sql': None, 'expected': 'msg=增加成功'}
    # data['params'] = eval(data['params'].encode('utf-8').decode('latin1'))
    # from common.configUtils import ConfigUtils
    from common.dataUtils import DataUtils

    sheets = eval(ConfigUtils().get_config_value('excel_case', 'SheetName'))
    for sheet in sheets:
        data = DataUtils(sheet).testCaseDataList()
        rr = RequestUtils().request_by_step(data)
        print(rr)

    url = 'https://t2wxapi.sancell.top/ssxq/w/auth/appPhoneLogin'
    parms = "{'phone': '16621080711', 'referrer_mem_id': '', 'ver_code': '8888'}"
    res = requests.post(url, parms)
    a = json.loads(parms)
    print(a)
