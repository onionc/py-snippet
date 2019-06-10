# coding:utf-8
""" 多抓鱼登录 使用cookies """

import requests
import json
import logging
from duozhuayu.xjs import get_token
from duozhuayu.proxy import Proxy
import telnetlib
logging.basicConfig(level=logging.DEBUG)


class Duozhuayu(object):
    def __init__(self):

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
        }
        self.proxy_list = None
        self.proxy_ip = None
        self.proxies = None
        #self.proxies = {"http":"http://117.36.103.170:8118"}
        self.allow_max_error_count = 2

    def get(self, url, proxy=False):
        logging.debug(f"request params: headers:{self.headers} proxies:{self.proxies}")
        try:
            resp = requests.get(url, verify=False, headers=self.headers, proxies=self.proxies, timeout=10)
        except Exception as e:
            resp = self.try_proxy_get()

        if resp.status_code == 429:
            # 访问额度用完
            resp = self.try_proxy_get()

        if resp.status_code == 200:
            return json.loads(resp.text)
        else:
            self.allow_max_error_count -= 1

            logging.info(f"http request error, code: {resp.status_code}")
            try:
                logging.info(f"error_data {json.loads(resp.text)}")
            except Exception as _:
                pass
            return False

    def try_proxy_get(self):
        """ 尝试代理请求 """
        self.try_get_proxy_ip()
        return requests.get(url, verify=False, proxies=self.proxies, headers=self.headers,timeout=10)

    def try_get_proxy_ip(self):
        """ 尝试代理ip """
        while self.allow_max_error_count:
            # 在允许出错次数内
            self.proxy_ip = self.get_proxy()
            if self.check_proxy_ip():
                logging.info(f"NO AUTH: set proxy_ip: {self.proxy_ip}")
            else:
                logging.info('proxy_ip error')
                self.allow_max_error_count -= 1
                continue

            # 可选代理
            if self.proxy_ip:
                self.proxies = {
                    'https': "https://" + self.proxy_ip
                }
                self.headers = self.assem_headers()
                logging.debug("try try_get_proxy_ip success ")
                return True

        logging.debug("try try_get_proxy_ip error")
        return False

    def login(self):
        """ 通过Cookie 登录 """
        self.headers['Cookie'] = '_ga=GA1.2.1145311583.1545965438; _gid=GA1.2.1993378194.1545965438; fish_c0="2|1:0|10:1545965455|7:fish_c0|24:NzM3Nzk0ODEyMTQ0NTIyNjI=|0ee1411db5fee11ec340cfd8859d713eb20a1881b570261bf0045177c10ba028"'
        user_info = y.get('https://www.duozhuayu.com/api/user')
        if user_info:
            return user_info
        else:
            return None

    def get_all_title(self, data):
        """ 获取所有书名 """
        return [i['item']['title'] for i in data['data'] if i['type']=='book']

    def assem_headers(self):
        """ 获取token, 组装header """
        x_data = get_token()
        x_data = {k: str(v) for k, v in x_data.items()}

        headers = {
            'x-api-version': '0.0.5',
            'x-refer-request-id': '0-1546336702230-61023',
            'x-request-id': '0-1546336702230-17714',
            'x-request-misc': '{"platform":"browser"}',
            'x-request-page': '/categories/135481276860730989',
            'x-request-token': x_data['token'],
            'x-security-key': x_data['security'],
            'x-timestamp': x_data['time'],
            'x-user-id': x_data['uid']
        }
        return headers

    def get_page_data(self):
        """ 获取分页数据 """
        next_url = None

        while True:
            logging.debug(f"next_url:{next_url}")
            url = yield next_url
            if not url:
                return
            logging.debug(f"url:{url}")

            headers = self.assem_headers()
            logging.debug(f"headers:{headers}")
            for k, v in headers.items():
                self.headers[k] = v
            
            data = self.get(url)

            if data:
                logging.info(f"{url} data:{len(data['data'])}, books title:{self.get_all_title(data)}")
                try:
                    next_url = data['paging']['next']
                except KeyError:
                    next_url = None

    def get_data(self, pages, url_primer):
        """ 获取pages页数的数据 """
        url_generator = self.get_page_data()
        url_generator.send(None)
        url = url_primer
        for _ in range(pages):
            if not url:
                break
            url = url_generator.send(url)

    def get_proxy(self):
        """ 从代理池拿到IP，因为代理池的都是些坏的，就用了一个有效的用来测试 """
        return '61.145.182.27:53281'

        if not self.proxy_list:
            self.proxy_list = Proxy().get()
        ip = None
        try:
            ip = self.proxy_list.pop()
        except IndexError as e:
            logging.debug("get_proxy error: " + e)
        return ip

    def check_proxy_ip(self):
        """ 验证IP是否可用 """
        if not self.proxy_ip:
            self.proxy_ip = self.get_proxy()
        if self.proxy_ip:
            ip, port = self.proxy_ip.split(':')
            logging.debug(f"check ip {ip}:{port}")
            try:
                telnetlib.Telnet(ip, port, timeout=10)
            except Exception as e:
                logging.debug('error')
                self.proxy_ip = None
                return False
                # self.check_proxy_ip()
            else:
                return True


if __name__ == '__main__':
    y = Duozhuayu()

    # 使用cookie登录
    # y.login()

    # 生成token获取分类数据
    url = 'https://www.duozhuayu.com/api/categories/135481276860730989/items?'
    y.get_data(3, url)








