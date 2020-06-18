import requests
from common.logger import Mylog

# 去除异常提示 https ssl
requests.packages.urllib3.disable_warnings()
log=Mylog()

class http_request:

    @staticmethod
    def httprequest(url, data, method, token, header='application/json'):
        header = {"Accept": "*/*",
                  "Content-Type": header + ";charset=utf8", "Authorization": "Bearer " + token}
        log.info('param：{}'.format(data))
        log.info('header:{}'.format(header))
        try:
            if method.lower() == 'get':
                res = requests.get(url, data, headers=header, verify=False)
                # if res.json()['data']['access_token']:
                #     setattr(Gettoken, 'TOKEN', res.json()['data']['access_token'])

            elif method.lower() == 'post':

                res = requests.post(url, data=data, headers=header,
                                    verify=False)
                # if res.json()['data']['access_token']:
                #     setattr(Gettoken, 'TOKEN', res.json()['data']['access_token'])

            elif method.lower() == 'delete':

                res = requests.delete(url, data=data, headers=header,
                                      verify=False)
                # if res.cookies:
                #     setattr(Gettoken, 'TOKEN', res.cookies)

            elif method.lower() == 'put':

                res = requests.put(url, data=data, headers=header,
                                   verify=False)
                # if res.cookies:
                #     setattr(Gettoken, 'TOKEN', res.cookies)

            else:
                print('请求方式异常')
        except Exception as e:
            print('请求异常：{}'.format(e))
            raise e

        log.info('response:{}'.format(res.json()))
        return res.json()


class Gettoken:
    TOKEN = '54ca2a57-03c8-429d-9a77-f717a5f7eabb'
    caselist = None


if __name__ == '__main__':
    data = '''{"loginName":"15639297807",
    "password":"f7a9e24777ec23212c54d7a350bc5bea5477fdbb","aikangNumber":"f0974aec1ede3640a78d01fa3934d0f510303e5d618cdc489de25c126750f004b04d6d8e56e1a21438c49cb71f07e56f"}'''
    url = 'https://api-uat.daoyitong.com/api/v1/account/login'
    rr = http_request.httprequest(url, data, 'post')
    print(rr.json())
