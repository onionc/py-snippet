> **引言** 这个游戏加点很烦人，每次开局都点的手累；小鼹鼠的礼物不在游戏界面就收不到，何不挂机。

### 测试

#### 图像匹配测试

截取了主界面全屏，

<img src="http://image.acfuu.com/mdImages/201811/home.png" style="width:600px">

从中截取了里面的小豆豆图像![pea_bad](http://image.acfuu.com/mdImages/201811/pea_bad.png)。
使用模板匹配，相似度总是0.55左右，[模板匹配(Match Template)](https://www.cnblogs.com/xrwang/archive/2010/02/05/MatchTemplate.html)中了解到工作原理：

> 通过在输入图像上滑动图像块对实际的图像块和输入图像进行匹配

大概知道了原因，小豆图片是直接从电脑上截取主界面图中的一小块，但是没有保持原分辨率，所以匹配不到。原图大小再截取了一次![pea](http://image.acfuu.com/mdImages/201811/pea.png)。匹配到相似度`0.9988448023796082`。

<img src="http://image.acfuu.com/mdImages/201811/blend_home.png" style="width:600px">

```python
# imread()函数读取目标图片和模板，目标图片先读原图，后灰度。灰度用来比较，原图用来标记匹配
img_bgr = cv2.imread("home.png")
img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
template = cv2.imread('pea.png', 0)
w, h = template.shape[::-1]

# 模板匹配
res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)

# 阈值
threshold = 0.9
loc = np.where( res >= threshold)

# 使用灰度图像中的坐标对原始RGB图像进行标记

for pt in zip(*loc[::-1]):
    cv2.rectangle(img_bgr, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

# 显示图像    

#cv2.namedWindow('blend', 0)
cv2.imshow('blend', img_bgr)
cv2.imwrite('./run_image/blend_home.png', img_bgr)
cv2.waitKey(0)
cv2.destroyAllWindows()
```
注：[OpenCV使用BGR而非RGB格式](https://www.cnblogs.com/pluviophile/p/opencv-bgr.html)

#### adb截图测试

adb截图命令很方便

1. 截图保存到sdcard
  `adb shell /system/bin/screencap -p /sdcard/screenshot.png`
2. pull拉取到本地
  `adb pull /sdcard/screenshot.png`

封装一下路径等变量：
```python
def execute(self, command):
    """ 执行adb命令 """
    command = "{} {}".format(self.adb_file_path, command)
    logging.info(command)
    os.system(command)

def get_screenshot(self, name):
    """ 获取屏幕截图 """
    self.execute(' shell screencap -p /sdcard/%s' % str(name))
    self.execute(' pull /sdcard/{0} {1}{0}'.format(name, self.run_image_path))
```

```
INFO:root:f:\py\wechat_rainbow/adb/adb   shell screencap -p /sdcard/rainbow_screen.png
INFO:root:f:\py\wechat_rainbow/adb/adb   pull /sdcard/rainbow_screen.png f:\py\wechat_rainbow/run_image/rainbow_screen.png
```

#### 封装公共函数


上一节封装了执行adb命令和获取屏幕截图函数。
要能进行下去还需两个核心函数：判断在某个界面，获取某个特征匹配中心点。

在界面中还需细分：一些异常会导致遮挡屏幕（被外部应用遮挡，比如被电话、视频打断）、（内部遮挡[不合预期的弹出]：送钻石的气球乱飘，误点到或者错误计算的位置误点弹出界面）。
![rainbowrp](http://image.acfuu.com/mdImages/201811/rainbowrp.png)



*主要功能列表*
- [x] 执行adb
- [x] 获取屏幕截图
- [x] 界面匹配
- [x] 特征按钮匹配
- [ ] 金币获取
- [x] 鼹鼠匹配
- [x] 执行动作（基础功能）

### 实战

#### 小鼹鼠的礼物

获取鼹鼠位置，

鼹鼠模板![mole.png](http://image.acfuu.com/mdImages/201811/mole.png)有时不能匹配上，发现鼹鼠是动的，比如![except_mole.png](http://image.acfuu.com/mdImages/201811/except_mole.png)就是异常的。异常匹配0.86不到0.9，故检测鼹鼠时，阈值降低至0.8。

矩阵最值
```
min_val,max_val,min_indx,max_indx=cv2.minMaxLoc(res)
```

点击鼹鼠领取礼物之后，弹出**「太棒了」**按钮，点击之后，有一定几率还是会出现一张地图的**「太棒了」**，所以太棒了得判断两次。

封装一个`checks (action, is_check, num=1)`方法，执行某动作多次用，并可选择是否点击。所有动作都可调用此基础方法，鼹鼠匹配的阈值不一样，则多加一个关键字参数。

```python
def checks(self, action, is_click=True, num=1, **kw):
    """ 检测多次动作"""
    for i in range(num):
        self.get_screenshot()
        
        if 'threshold' in kw:
            threshold = kw['threshold']
        else:
            threshold = self.default_threshold

        good_co = self.match(action, threshold)
        if not good_co:
            logging.info(str(action) + "未找到")
            return
        if is_click:
            self.click(*good_co[0])
        logging.info("{0} ok! ({1}/{2})".format(action, i+1, num))
        time.sleep(1)
```

这样子挖钻石就很简单清晰了

```python
def mole(self):
    """ 挖钻石 """
    if self.checks('home', is_click=False):
        # 主界面
        if self.checks('mole', threshold=0.8):
            # 鼹鼠界面
            if self.checks('good', num=2, screen=True):
                # 太棒了界面
                logging.info('领取成功')
```

到这里鼹鼠送的钻石和金币就可以领取成功了。如果要深入自动化玩法，还包括收割金币，加点。

金币可以用金币模板![gold.png](http://image.acfuu.com/mdImages/201811/gold.png)匹配到<img src="http://image.acfuu.com/mdImages/201811/match_gold.png" style="width:600px">，看得出多个目标都可匹配（每个金币可能会有>=3个坐标点），匹配多个目标的返回值就得用`np.where`返回多坐标。


### 参考资料
- [使用Python+OpenCV进行图像模板匹配(Match Template)](http://www.51testing.com/html/01/n-3721401.html)

- [模板匹配(Match Template)](https://www.cnblogs.com/xrwang/archive/2010/02/05/MatchTemplate.html)

- [Android之用adb screencap -p命令截图](https://blog.csdn.net/u011068702/article/details/74456109)
