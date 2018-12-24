# coding:utf-8
""" 调用迅雷下载 """
import subprocess
import base64


class Thunder(object):
    def __init__(self):
        self.thunder_path = r'C:\Program Files (x86)\Thunder Network\Thunder\Program\Thunder.exe'

    def Url2Thunder(self, url):
        url = 'AA' + url + 'ZZ'
        url = base64.b64encode(url.encode('ascii'))
        url = b'thunder://' + url
        thunder_url = url.decode()
        return thunder_url

    def download_with_thunder(self, file_url, cover_url=True):
        if cover_url:
            thunder_url = self.Url2Thunder(file_url)
        else:
            thunder_url = file_url
        subprocess.call([self.thunder_path, thunder_url])
