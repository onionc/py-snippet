# coding:utf-8
""" 爬取豆瓣土味情话 """
from module.download import Download
import re
import sys

if __name__ == '__main__':
    # 爬取文本

    # 1 https://www.guaze.com/juzi/16832.html 这个数据特殊，保存用ISO 8859-1, 打开用GB2312
    # 使用：第一次不开启debug，将会写入文件，之后开启debug可用文件分析。
    # down = Download(file_name=sys.path[0]+'/whisper1.html', encoding='ISO 8859-1')
    down = Download(file_name=sys.path[0]+'/whisper1.html', encoding='GB2312', debug=True)  # 第二次可加debug=True, 用文件调试，避免直接请求
    html = down.get_text('https://www.guaze.com/juzi/16832.html', re.compile(r'\<p\>(\d+)[、]?((.*)(?=www)|(.*)(<\/p>))', re.I))
    # 处理数据
    html = [i[3] for i in html]
    # 写入文件
    down.save(sys.path[0]+"/whispers.txt", html)

    # 2 https://baijiahao.baidu.com/s?id=1612847567100515849&wfr=spider&for=pc
    # down = Download(file_name=sys.path[0]+'/whisper2.html')
    down = Download(file_name=sys.path[0]+'/whisper2.html', debug=True)
    html = down.get_text('https://baijiahao.baidu.com/s?id=1612847567100515849&wfr=spider&for=pc', '.bjh-p')
    # 处理数据
    html = '\n'.join([i.get_text() for i in html])
    html = re.findall(r'\d+[、](.*)', html)
    # 写入文件
    down.save(sys.path[0]+"/whispers.txt", html)
