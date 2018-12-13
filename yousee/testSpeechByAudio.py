# coding:utf-8

"""
实时语音识别测试
"""
import speech_recognition as sr
import logging
logging.basicConfig(level=logging.DEBUG)

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
    print(test)
    logging.info('end')
