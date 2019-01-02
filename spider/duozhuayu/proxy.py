# coding:utf-8
""" 代理IP """
import requests
from random import randint
import re


class Proxy(object):
    def __init__(self):
        self.target = f"https://www.xicidaili.com/nn/{randint(0, 100)}"  # http://www.data5u.com/free/index.html
        self.headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"}

    def get(self):
        resp = requests.get(self.target, headers=self.headers, verify=False)
        data = resp.text
        ip_list = re.findall(r'((\d{1,3}\.){3}\d+)[^\d]+(\d+)', data)
        proxy_list = [f"{i[0]}:{i[2]}" for i in ip_list]
        return proxy_list


if __name__ == "__main__":
    data = Proxy().get()
    print(data)
