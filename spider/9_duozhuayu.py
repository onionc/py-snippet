# coding:utf-8
""" 多抓鱼登录 使用cookies """

import requests
import json
import logging
logging.basicConfig(level=logging.DEBUG)
from duozhuayu.xjs import get_token


class Duozhuayu(object):
    def __init__(self):

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
        }

    def get(self, url):
        resp = requests.get(url, headers=self.headers, verify=False)
        if resp.status_code != 200:
            logging.info(f"http request error, code: {resp.status_code}")
            try:
                logging.info(f"error_data {json.loads(resp.text)}")
            except Exception as _:
                pass
            return False

        return json.loads(resp.text)

    def login(self):
        """ 通过Cookie 登录 """
        self.headers['Cookie'] = '_ga=GA1.2.1145311583.1545965438; _gid=GA1.2.1993378194.1545965438; fish_c0="2|1:0|10:1545965455|7:fish_c0|24:NzM3Nzk0ODEyMTQ0NTIyNjI=|0ee1411db5fee11ec340cfd8859d713eb20a1881b570261bf0045177c10ba028"'
        user_info = y.get('https://www.duozhuayu.com/api/user')
        if user_info:
            return user_info
        else:
            return None

    def get_page_data(self, headers):
        """ 获取分页数据 """
        for k, v in headers.items():
            self.headers[k] = v

        url = "https://www.duozhuayu.com/api/categories/135481276860730989/items?"
        data = self.get(url)
        if data:
            logging.info(f"{url} data:{len(data['data'])}")


if __name__ == '__main__':
    y = Duozhuayu()
    # y.login()

    # 分类数据获取

    ## 获取token
    x_data = get_token()
    x_data = {k: str(v) for k, v in x_data.items()}

    headers={
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
    
    y.get_page_data(headers)








