#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author    : zhaofy
# @Datetime  : 2020/7/24 17:42
# @File      : Assert.py
# @desc      :

import json
from common.logger import Mylog

logger = Mylog()


def Assert(expected, res):
    exp = {}
    if expected:
        for i in expected.strip().split(','):
            exp[i.split('=')[0]] = i.split('=')[1]
    else:
        pass
    try:
        for k, v in exp.items():
            if k == 'status_code':
                reslut = str(res.status_code)
                assert v == str(res.status_code)
            else:
                reslut = str(res.json()[k])
                assert v == str(res.json()[k])
        return [True, k, v, reslut]
    except AssertionError:
        return [False, k, v, reslut]


if __name__ == '__main__':
    a = {'sheetname': 'product', 'caseid': '3', 'tag': '保存分类', 'url': 'http://192.168.200.104:9900/api-product-admin/category',
         'method': 'post',
         'header': {'Authorization': 'Bearer 02f21152-abfd-461f-ab2f-9f3cfd4cbf2e', 'Content-Type': 'application/json'},
         'params': b'{\n  "cdesc": "\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe5\xae\xb9\xe6\x8a\xa4\xe8\x82\xa4\xe4\xb8\x8d\xe4\xba\x8c\xe4\xb9\x8b\xe9\x80\x89\xef\xbc\x8c\xe8\xbf\x98\xe4\xbd\xa0\xe5\xa4\xa9\xe4\xbd\xbf\xe5\xae\xb9\xe9\xa2\x9c\xef\xbc\x8c\xe5\x8f\x98\xe7\xbe\x8e\xe4\xb8\x8d\xe5\xae\xb9\xe9\x94\x99\xe8\xbf\x87\xef\xbc\x8c\xe5\x88\xab\xe8\xae\xa9\xe8\x87\xaa\xe5\xb7\xb1\xe5\x90\x8e\xe6\x82\x94\xe3\x80\x82\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd",\n  "chidden": 1,\n  "ckeywords": "\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8,\xe7\xbe\x8e\xe7\x99\xbd,\xe6\x8a\xa4\xe8\x82\xa4,\xe6\x8a\x97\xe8\xa1\xb0\xe8\x80\x81,\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd,\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd,\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd,\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd,\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd,\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd,\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd",\n  "clevel": "L1v\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbdo(\xe2\x88\xa9_\xe2\x88\xa9)o \xe5\x93\x88\xe5\x93\x88\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd1002020303610\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x99\xbd",\n  "cname": "\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbdo(\xe2\x88\xa9_\xe2\x88\xa9)o \xe5\x93\x88\xe5\x93\x88\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd\xe7\x8e\xbb\xe5\xb0\xbf\xe9\x85\xb8\xe7\xbe\x8e\xe7\x99\xbd10020",\n  "createTime": "2020-06-16T18:10:09.076Z",\n  "deleted": 0,\n  "iconUrl": "mlwl.oss-cn-shanghai.aliyuncs.com/\xe7\xba\xa2\xe5\x8c\x85\xe8\xb5\x84\xe9\x87\x91\xe6\xb5\x81\xe7\xa8\x8b\xe5\x9b\xbe.png",\n  "picUrl": "mlwl.oss-cn-shanghai.aliyuncs.com/WechatIMG41.png",\n  "id":100202036,\n  "pid": -1,\n  "sortOrder": 111,\n  "updateTime": "2020-06-15T18:10:09.076Z"\n}',
         'response': None, 'sql': None, 'expected': 'resp_code=1'}
    b = a['params']
    b = eval(b)
    print(b)