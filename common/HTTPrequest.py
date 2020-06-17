import requests


class http_request:

    @staticmethod
    def httprequest(url, data, method, cookies):
        header = {"Accept": "*/*",
                  "Content-Type": "application/json;charset=utf8"}
        try:
            if method == 'get':
                res = requests.get(url, data, verify=False,
                                   cookies=getattr(Gettoken, 'TOKEN'))
                if res.cookies:
                    setattr(Gettoken, 'TOKEN', res.cookies)


            elif method == 'post':

                res = requests.post(url, data=data, headers=header,
                                    cookies=getattr(Gettoken, 'TOKEN'),
                                    verify=False)
                if res.cookies:
                    setattr(Gettoken, 'TOKEN', res.cookies)
            else:
                print('请求方式异常')
        except Exception as e:
            print('请求异常：{}'.format(e))
            raise e

        return res


class Gettoken:
    TOKEN = None


if __name__ == '__main__':
    data = '''{"loginName":"15639297807",
    "password":"f7a9e24777ec23212c54d7a350bc5bea5477fdbb","aikangNumber":"f0974aec1ede3640a78d01fa3934d0f510303e5d618cdc489de25c126750f004b04d6d8e56e1a21438c49cb71f07e56f"}'''
    url = 'https://api-uat.daoyitong.com/api/v1/account/login'
    rr = http_request.httprequest(url, data, 'post')
    print(rr.json())
