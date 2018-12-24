# coding:utf-8
import requests
from bs4 import BeautifulSoup
from collections import Counter


def get_count(data):
    """ 获取元素出现次数最多的前5名 """
    count = Counter(data)
    count = count.most_common(5)
    return dict(count)


html = requests.get('https://www.yukunweb.com/2017/6/python-spider-BeautifulSoup-basic/')
content = html.text

soup = BeautifulSoup(content, 'lxml')
codes = soup.find_all('code')
top5 = get_count(codes)
print(top5)