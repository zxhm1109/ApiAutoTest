#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author    : zhaofy
# @Datetime  : 2020/8/11 17:40
# @File      : spider.py
# @desc      :

import requests
from queue import Queue
from threading import Thread as Task
import time
import random
salebilllist=[]

class Spider():
    def __init__(self, base_url, headers, data,flag=1):
        self.base_url = base_url
        self.headers = headers
        self.data = data
        self.flag=flag
        self.url_queue = Queue()
        self.html_queue = Queue()
        self.item_queue = Queue()
        self.proxies = []
        self.idx = 0


    def update_proxy_ip(self):
        response = requests.get('http://ip.16yun.cn:817/myip/pl/fc90ef80-9a6c-40ce-9ed1-9734637649c0/?s=wdpfberipq&u=ggz')
        self.proxies = response.text.split('\r\n')
        print(self.proxies)

    def get_url_list(self):
        '''
        生产 url 并且放入到队列中
        :return:
        '''
        for idx in range(100000):
            self.url_queue.put(self.base_url)

    def get_html(self):
        '''
        从 url 队列中取 url 获取 html
        把 html 放入到 html 队列中
        :param url:
        :return:
        '''

        while True:
            url = self.url_queue.get()
            response = requests.post(
                url=url,
                headers=self.headers,
                data=self.data,
                proxies={
                    'http': self.proxies[self.idx % 100]
                }
            )
            self.idx = self.idx + 1

            try:
                if response.status_code == 200:
                    result = response.json()
                    print('result:', result)
                    if self.flag ==0:
                        salebill=result['content']['salebill_id']
                        salebilllist.append(salebill)
                        print('创建订单：{}'.format(salebill))
                    self.html_queue.put(result)
                else:
                    print('操作失败:', response.text)
            except Exception as e:
                print("异常：", e)
            time.sleep(1)
            self.url_queue.task_done()

    def get_items(self):
        '''
        从 html 队列中获取html
        解析获取 item
        把 item放入到 item队列中

        :param html:
        :return:
        '''
        while True:
            html = self.html_queue.get()
            # eroot = etree.HTML(html)
            # results = eroot.xpath('//a[@class="recmd-content"]/text()')
            # for result in results:
            #     item = {}
            #     item["title"] = result
            #     self.item_queue.put(item)

            self.html_queue.task_done()

    def save_item(self):
        '''
        从队列中取 item 保存
        :param item:
        :return:
        '''
        while True:
            item = self.item_queue.get()
            print(item)
            print("*" * 100)
            self.item_queue.task_done()

    def run(self):

        tasks = []

        self.update_proxy_ip()

        get_url_task = Task(target=self.get_url_list)
        tasks.append(get_url_task)

        for i in range(500):
            get_html_task = Task(target=self.get_html)
            tasks.append(get_html_task)

        for i in range(100):
            get_items_task = Task(target=self.get_items)
            tasks.append(get_items_task)

        for i in range(100):
            save_item_task = Task(target=self.save_item)
            tasks.append(save_item_task)

        for task in tasks:
            task.setDaemon(True)
            task.start()

        time.sleep(1)
        self.url_queue.join()
        self.html_queue.join()
        self.item_queue.join()
        pass


if __name__ == '__main__':
    from common.configUtils import yamlUtils
    url = yamlUtils().read(section='url1')
    print(url)
    # spider = Spider(url['base_url'], url['headers'], url['data'])
    # spider.run()
