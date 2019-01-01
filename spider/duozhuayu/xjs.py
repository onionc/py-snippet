import execjs
import os
import logging
logging.basicConfig(level=logging.DEBUG)
path1 = os.path.dirname(__file__)  # 当前路径


"""
    通过调用js, 获取token和加密数据
"""

def get_js(path, encodes='utf-8'):
    logging.debug("js file path is "+path)

    f = open(path, 'r', encoding=encodes)  # 打开JS文件
    line = f.readline()
    html_str = ''
    while line:
        html_str = html_str + line
        line = f.readline()
    return html_str

def load_sign_js(js_str):
    return execjs.compile(js_str)

def get_token():
    result = {}
    # get token
    sign_js_path = r'' + path1 + "\client.js"
    logging.info('get token js start.')
    sign_js = load_sign_js(get_js(sign_js_path, 'UTF-8'))
    logging.info('get token js ok.')
    data = sign_js.call('get_headers')
    return data
