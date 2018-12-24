# coding:utf-8

from bs4 import BeautifulSoup
import requests
from module.thunder import Thunder
import re
import html as Html
import logging
logging.basicConfig(level=logging.DEBUG)


class Download(object):
    def __init__(self, debug=False, file_name='test.html', encoding='utf-8'):
        self.debug = debug
        self.file_name = file_name
        self.encoding = encoding

    def get(self, url):
        """ 封装GET. 设置headers, 返回html串 """
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
        resp = requests.get(url, headers=headers)
        logging.info(f"{url} encoding is {resp.encoding}, will cover to {self.encoding}")
        resp.encoding = self.encoding

        if not self.debug:
            # 当未开启调试则写入文件，第二次好调用本地调试
            with open(self.file_name, 'w', encoding=self.encoding) as f:
                f.write(resp.text)

        return resp.text

    def html_parse(self, html, select, type="selector"):
        """ html解析 """

        soup = BeautifulSoup(html, 'lxml')
        if type == 'selector':
            content = soup.select(select)
        elif type == 'regular':
            content = soup.find_all(re.compile(select))
        return content

    def get_video(self, url, select, select2='href', start_index=None, end_index=None, step=1):
        """ 调用迅雷下载电影
            param:
                url 地址
                select 选择器
                select 第二次选择器标签，有的a中链接可能在 ed2k、href 标签中
                start_index:end_index:step 为列表切片
        """
        # 调试则用本地文件，否则抓取
        if self.debug:
            url = self.file_name
            with open(url, 'r', encoding=self.encoding) as f:
                html = f.read()
        else:
            html = self.get(url)

        content = self.html_parse(html, select)
        logging.debug("count:%s" % len(content))
        logging.debug(content)
        # 选取条数
        content = content[start_index:end_index:step]
        thunder = Thunder()
        for a in content:
            text = a.get_text()
            href = a.get(select2)
            logging.debug(f"{text}, {href}")
            thunder.download_with_thunder(href)

    def get_text(self, url, select):
        """ 获取文本 """
        # 调试则用本地文件，否则抓取
        if self.debug:
            url = self.file_name
            with open(url, 'rb') as f:
                html = f.read()
                html = html.decode(self.encoding, "ignore")
        else:
            html = self.get(url)

        if isinstance(select, re.Pattern):
            # 正则，直接使用
            content = select.findall(html)
        else:
            content = self.html_parse(html, select)
        logging.debug("count:%s" % len(content))
        logging.debug(content)
        return content

    def save(self, file, content):
        """ 保存文件 """
        with open(file, 'a', encoding='utf-8') as f:
            for i in content:
                if not i:
                    continue
                f.write(Html.unescape(i)+'\n')

