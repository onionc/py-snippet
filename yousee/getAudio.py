# coding:utf-8

"""
语音识别并响应。使用谷歌语音服务，不需要KEY（自带测试KEY）。https://github.com/Uberi/speech_recognition
"""
import speech_recognition as sr
import pyttsx3
import re
import logging
logging.basicConfig(level=logging.DEBUG)

resource = {
    r"(你看看?){1}.*\1": "我不看，再让我看打死你",
    r"(你看看?)+": "你看看你看看，操不操心",
    r"(你.+啥)+": "咋地啦",
    r"(六六六|666)+": "要不说磐石老弟六六六呢？",
    r"(磐|石|老|弟)+": "六六六",
}

engine = pyttsx3.init()

while True:
    r = sr.Recognizer()
    # 麦克风
    mic = sr.Microphone()

    logging.info('录音中...')
    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    logging.info('录音结束，识别中...')
    test = r.recognize_google(audio, language='cmn-Hans-CN', show_all=True)

    # 分析语音
    logging.info('分析语音')
    if test:
        flag = False
        message = ''
        for t in test['alternative']:
            logging.debug(t)
            for r, c in resource.items():
                # 用每个识别结果来匹配资源文件key(正则)，正确匹配则存储回答并退出
                logging.info(r)
                if re.search(r, t['transcript']):
                    flag = True
                    message = c
                    break
            if flag:
                break
        # 文字转语音
        if message:
            logging.info('bingo....')
            logging.warning('say: %s' % message)
            engine.say(message)
            engine.runAndWait()
            logging.info('ok')
    logging.info('end')
