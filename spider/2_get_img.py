# coding:utf-8
import requests
import os
import sys

url = 'http://docs.python-requests.org/zh_CN/latest/_static/requests-sidebar.png'
resp = requests.get(url)

img_name = os.path.basename(url)
img_path = sys.path[0]+'/'+img_name
# print(resp.content)
with open(img_path, 'wb') as f:
    f.write(resp.content)
    print(f"download image file : {img_path}")
