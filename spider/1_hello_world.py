# coding:utf-8
import requests

resp = requests.get('https://www.baidu.com', verify=False)
# html = resp.text.encode('ISO-8859-1').decode('utf-8')
# print(resp.encoding)
# print(html)
resp.encoding = 'utf-8'
print(resp.text)