import os
import sys
import cv2
import numpy as np
import time
import logging
logging.basicConfig(level=logging.DEBUG, filename='rain.log')


class Rainbow(object):

    def __init__(self):
        self.screen_base_img_name = 'rainbow_screen.png'  # 基础名称
        self.screen_current_img_name = self.screen_base_img_name  # 当前截图名称
        self.run_path = sys.path[0]
        self.adb_file_path = self.run_path+'/adb/adb '
        self.run_image_path = self.run_path+'/run_image/'
        self.data_image_path = self.run_path+'/data_image/'
        self.default_threshold = 0.9  # 默认阈值
        # 路由对应模板
        self.route_template = {
            'home': 'pea.png',
            'mole': 'mole.png',
            'good': 'good.png',
            'gold': 'gold.png',
            'cancel': 'cancel1.png'
        }
        pass

    def match(self, name, threshold=0):
        """ 匹配界面 """

        if threshold == 0:
            # 默认阈值
            threshold = self.default_threshold

        if name in self.route_template:
            # 判断每次图片路由
            template_img = self.route_template[name]
            return self.check_template(template_img, threshold)

    def check_template(self, t_img, threshold=0.9, debug=True):
        """ 页面匹配 

        Returns:
            None/[x,y]
        """
        coordinate = []

        # imread()函数读取目标图片和模板，目标图片先读原图，后灰度。灰度用来比较，原图用来标记匹配
        try:
            img_bgr = cv2.imread("{0}{1}".format(self.run_image_path, self.screen_current_img_name))
            img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
            template = cv2.imread("{0}{1}".format(self.data_image_path, t_img), 0)
            h, w = template.shape[:2]

            # 模板匹配
            res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)

        except Exception as e:
            logging.exception(e)
            raise

        # 矩阵最值
        min_val, max_val, min_indx, max_index = cv2.minMaxLoc(res)
        logging.info(cv2.minMaxLoc(res))
        if max_val > threshold and max_index:
            coordinate.append(max_index)

        # 阈值
        loc = np.where(res >= threshold)

        # 使用灰度图像中的坐标对原始RGB图像进行标记
        for pt in zip(*loc[::-1]):
            # coordinate.append((pt[0]+int(w/2), pt[1]+int(h/2)))
            if debug:
                cv2.rectangle(img_bgr, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

        if debug:
            # 显示图像
            # cv2.imshow('blend', img_bgr)
            cv2.imwrite('%s/test.png' % self.run_image_path, img_bgr)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

        if coordinate:
            return coordinate

    def execute(self, command):
        """ 执行adb命令 """
        command = "{} {}".format(self.adb_file_path, command)
        logging.info(command)
        os.system(command)
        time.sleep(0.5)

    def get_screenshot(self, name=''):
        """ 获取屏幕截图 """
        logging.info('截屏中，请等待')
        if not name:
            # 名称加时间戳
            self.screen_current_img_name = str(int(time.time())) + self.screen_base_img_name
        else:
            self.screen_current_img_name = str(int(time.time())) + name

        self.execute(' shell screencap -p /sdcard/%s' % str(self.screen_base_img_name))
        self.execute(' pull /sdcard/{0} {1}{2}'.format(
            self.screen_base_img_name,
            self.run_image_path,
            self.screen_current_img_name
        ))

        time.sleep(1)

    def click(self, w, h, press_time=0):
        """ 点击 """
        self.execute("shell input tap  {} {}".format(w, h))

    def checks(self, action, is_click=True, num=1, **kw):
        """ 匹配检测并执行

        Args:
            string action: 匹配模板名称
            boolean is_click: 是否点击
            int num: 执行多次
            dict kw:{
                float 'threshold':0.9 # 阈值
                boolean 'screen':True # 截屏
            }
        Returns:
            boolean
        """

        result = False

        for i in range(num):
            logging.info("[{0}] start! ({1}/{2}) {3}".format(action, i+1, num, kw))
            if 'screen' in kw and kw['screen']:
                self.get_screenshot()

            if 'threshold' in kw:
                threshold = kw['threshold']
            else:
                threshold = self.default_threshold

            good_co = self.match(action, threshold)
            if not good_co:
                logging.info(str(action) + "未找到")
            else:
                result = True
                if is_click:
                    self.click(*good_co[0])
            logging.info("{0} ok! ({1}/{2})".format(action, i+1, num))
            time.sleep(1)

        return result

    def mole(self):
        """ 挖钻石 """
        if self.checks('home', is_click=False):
            # 主界面
            if self.checks('mole', threshold=0.8):
                # 鼹鼠界面
                if self.checks('good', num=2, screen=True):
                    # 太棒了界面
                    logging.info('领取成功')

    def run(self):
        logging.info('run')
        # 首页判断
        # self.test('origin.png', 'home')
        # self.test('origin.png', 'mole')
        # self.test('test_mole_1.png', 'mole')
        # self.test('test_mole_2.png', 'mole')
        # mole_co = self.match('mole', 0.8)
        # self.checks('gold', is_click=False) # 金币匹配多个

        while True:
            logging.info('休眠...')
            time.sleep(30)
            # input('next:')
            logging.info('休眠结束，开始执行：截屏')
            self.get_screenshot(self.screen_base_img_name)
            logging.info('鼹鼠呢？')
            self.mole()


rainbow = Rainbow()
rainbow.run()
