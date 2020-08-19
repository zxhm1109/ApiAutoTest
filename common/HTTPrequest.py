import requests
import json, re
from common.DoConfig import *
import urllib3

# 去除异常提示 https ssl
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logger = Mylog()


class http_request:
    params = ''

    @classmethod
    def HttpReqest(cls, data):
        """解决请求前的参数问题：参数化、参数化格式"""
        pattern = re.compile('\${(.+?)}')

        for k, v in data.items():
            if v is not None and '$' in str(v):
                v = json.dumps(v)
                all = {}

                for ii in range(len(pattern.findall(v))):
                    a = pattern.findall(v)[ii]
                    value = str(ReadConfig.read_config('Base', a))
                    xxxx = re.compile('\${' + a + '}')
                    xx = xxxx.findall(v)
                    all[xx[0]] = value
                for kk, vv in all.items():
                    v = v.replace(kk, vv)
                data[k] = load_params(v)
                if k == 'header' and ('{' and '}') in v:
                    data[k] = load_params(eval(v))
            #  修改入参编码
            # if k == 'params' and v and ('{' or '}') in v:
            #     data[k] = eval(v)
            #     cls.params = data[k]
            #     data[k] = v.encode('utf-8').decode('latin1')
            #     data['params'] = data['params'].encode('utf-8')
            # else:
            #     cls.params = data['params']
        res = http_request.dorequest(data)
        return res

    @classmethod
    def dorequest(cls, data):
        # sheetname, caseid, tag, url, method, header, params, response, sql, expected = data
        logger.info('TestCase:{} Request url:{}, Parameters:{},header:{} '.format(data['tag'], data['url'], data['params'],
                                                                                  type(data['header'])))
        if data['method'].lower() == 'get':
            res = requests.get(data['url'], data=data['params'], headers=data['header'], verify=False)
            return res
        elif data['method'].lower() == 'post':
            res = requests.post(data['url'], data=data['params'], headers=data['header'], cookies=None,
                                verify=False)
            return res
        elif data['method'].lower() == 'delete':
            res = requests.delete(data['url'], data=data['params'], headers=data['header'],
                                  verify=False)
            return res
        elif data['method'].lower() == 'put':
            res = requests.put(data['url'], data=data['params'], headers=data['header'],
                               verify=False)
            return res
        else:
            print('请求方式异常')


def load_params(params):
    # if ('{' or '}') in params:
    params = eval(params)
    #     return params
    # else:
    return params


if __name__ == '__main__':
    # data = 'username=user&password=123456&validCode=pyqg&deviceId=12321312asdadasda11111&grant_type=password_code'
    # url = 'http://192.168.200.203:9900/api-uaa/oauth/token'
    # header = {
    #     'Authorization': 'Basic d2ViQXBwOndlYkFwcA==',
    #     'Content-Type': 'application/x-www-form-urlencoded'
    # }

    data = {'sheetname': 'login', 'caseid': 'login_1', 'tag': '账号密码登录', 'url': 'https://t2wxapi.sancell.top//ssxq/w/auth/pin',
            'method': 'post', 'header': {'Content-Type': 'application/json;charset=UTF-8',
                                         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'},
            'params': '{"phone": "17621757807","pin_type": "login"}',
            'response': None, 'sql': None, 'expected': 'msg=增加成功'}
    # data['params'] = eval(data['params'].encode('utf-8').decode('latin1'))
    rr = http_request.dorequest(data)
    print(rr.text)

    # data = {'sheetname': 'product', 'caseid': '3', 'tag': '保存分类', 'url': 'http://192.168.200.104:9900/api-product-admin/category',
    #         'method': 'post',
    #         'header': {'Authorization': 'Bearer 02f21152-abfd-461f-ab2f-9f3cfd4cbf2e', 'Content-Type': 'application/json'},
    #         'params': b'{\n  "cdesc": "\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe5\xae\xb9\xe6\x8a\xa4\xe8\x82\xa4\xe4\xb8\x8d\xe4\xba\x8c\xe4\xb9\x8b\xe9\x80\x89\xef\xbc\x8c\xe8\xbf\x98\xe4\xbd\xa0\xe5\xa4\xa9\xe4\xbd\xbf\xe5\xae\xb9\xe9\xa2\x9c\xef\xbc\x8c\xe5\x8f\x98\xe7\xbe\x8e\xe4\xb8\x8d\xe5\xae\xb9\xe9\x94\x99\xe8\xbf\x87\xef\xbc\x8c\xe5\x88\xab\xe8\xae\xa9\xe8\x87\xaa\xe5\xb7\xb1\xe5\x90\x8e\xe6\x82\x94\xe3\x80\x82\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd",\n  "chidden": 1,\n  "ckeywords": "\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8,\xe7\xbe\x8e\xe7\x99\xbd,\xe6\x8a\xa4\xe8\x82\xa4,\xe6\x8a\x97\xe8\xa1\xb0\xe8\x80\x81,\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd,\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd,\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd,\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd,\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd,\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd,\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd",\n  "clevel": "L1v\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbdo(\xe2\x88\xa9_\xe2\x88\xa9)o \xe5\x93\x88\xe5\x93\x88\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd1002020303610\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x99\xbd",\n  "cname": "\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbdo(\xe2\x88\xa9_\xe2\x88\xa9)o \xe5\x93\x88\xe5\x93\x88\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd10020",\n  "createTime": "2020-06-16T18:10:09.076Z",\n  "deleted": 0,\n  "iconUrl": "mlwl.oss-cn-shanghai.aliyuncs.com/\xe7\xba\xa2\xe5\x8c\x85\xe8\xb5\x84\xe9\x87\x91\xe6\xb5\x81\xe7\xa8\x8b\xe5\x9b\xbe.png",\n  "picUrl": "mlwl.oss-cn-shanghai.aliyuncs.com/WechatIMG41.png",\n  "id":100202036,\n  "pid": -1,\n  "sortOrder": 111,\n  "updateTime": "2020-06-15T18:10:09.076Z"\n}',
    #         'response': None, 'sql': None, 'expected': 'resp_code=1'}
    #
    # http_request.HttpReqest(data)
