# coding:utf-8
""" 下载资源 """
from module.download import Download


if __name__ == '__main__':
    # 红楼
    hl_down = Download(file_name='hl.html', encoding='GB2312')  # 第二次可加debug=True, 用文件调试，避免直接请求
    hl_down.get_video(
        'https://m.2011mv.com/res/6154/',
        '.download_list .download_title > a')

    # 风骚律师 第三季
    hl_down = Download(file_name='fxlo3.html', encoding='GB2312')
    hl_down.get_video(
        'https://m.2011mv.com/res/13969/',
        '.introtext table a',
        'href',
        10, 20)