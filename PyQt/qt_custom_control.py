import sys
from PyQt5.QtWidgets import QWidget, QApplication, QSlider, QApplication, \
                            QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import QObject, Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QFont, QColor, QPen

class Communicate(QObject):
    '''
        自定义updateBW信号
    '''
    updateBW =pyqtSignal(int)

class BurningWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 设置控件最小的宽度和高度
        self.setMinimumSize(1,30) 
        self.value=75
        # 刻度值
        self.num=[75, 150, 225, 300, 375, 450, 525, 600, 675]

    def setValue(self,value):
        self.value=value

    def paintEvent(self,e):
        '''
        更新窗口
        每次更改窗口大小，切换窗口，都会触发；单纯移动不会出触发；
        移动里面Slider也不会主动触发，所以Example.changeValue()里主动调用控件的repaint或者update，以重新绘制
        '''
        #print("--update show --")
        qp=QPainter()
        qp.begin(self)
        self.drawWidget(qp)
        qp.end()

    def drawWidget(self,qp):
        '''
            自定义控件的核心绘制
        '''
        #(700,750)区间为烧毁范围
        MAX_CAPACITY=700
        OVER_CAPACITY=750

        font = QFont('Serif',7,QFont.Light)
        qp.setFont(font)

        # 当前窗口大小，step为宽度的1/10，刻度值self.num分割这十份宽
        size=self.size()
        w=size.width()
        h=size.height()
        step=int(round(w/10))
        #print("step:",step)

        # till当前值对应的控件渲染宽度，full正常烧录能达到的最大宽
        till = int(((w / OVER_CAPACITY) * self.value))
        full = int(((w / OVER_CAPACITY) * MAX_CAPACITY))
        #print(self.value,till,full)
        if self.value >= MAX_CAPACITY:
            # 当值大于最大MAX，则将MAX部分的全部渲染(宽度为full)
            qp.setPen(QColor(255, 255, 255))
            qp.setBrush(QColor(255, 255, 184))
            qp.drawRect(0, 0, full, h)
            # 其他部分，为烧毁的部分，用另一个颜色渲染
            qp.setPen(QColor(255, 175, 175))
            qp.setBrush(QColor(255, 175, 175))
            qp.drawRect(full, 0, till-full, h)
        else:
            # 正常烧录
            qp.setPen(QColor(255, 255, 255))
            qp.setBrush(QColor(255, 255, 184))
            qp.drawRect(0, 0, till, h)

        # 画笔设置，画刷无
        pen = QPen(Qt.black, 1, Qt.SolidLine)
        qp.setPen(pen)
        qp.setBrush(Qt.NoBrush)
        # 外层边框
        qp.drawRect(0, 0, w-1, h-1)

        # 刻度的绘制
        j = 0
        for i in range(step, 10*step, step):

            # 刻度竖线
            qp.drawLine(i, 0, i, 5)
            
            # 这里使用字体去渲染文本。必须要知道文本的宽度，这样才能让文本的中间点正好落在竖线上。
            metrics = qp.fontMetrics()
            fw = metrics.width(str(self.num[j]))
            qp.drawText(i-fw/2, h/2, str(self.num[j])) 
            # 使用重载函数 void QPainter::drawText(int x, int y, const QString &text) 位置(x,y)处绘制text
            # i为竖线位置，fw为字体宽度（fw/2为字体中间位置），i-fw/2则把数字的左半长度移动到了刻度左边，居中！
            
            j = j + 1

class Example(QWidget):
    
    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):      

        OVER_CAPACITY = 750
        
        # 放置上侧滑块
        sld = QSlider(Qt.Horizontal, self)
        #sld.setFocusPolicy(Qt.NoFocus)
        sld.setRange(1, OVER_CAPACITY)
        sld.setValue(75)
        sld.setGeometry(30, 40, 150, 30)

        # 创建信号和控件
        self.c = Communicate()        
        self.wid = BurningWidget()

        # 将滑块改变与self.changeValue方法绑定，当滑块滑动，执行changValue方法，在方法中，手动调用信号更新，所以下面的信号也会更新
        sld.valueChanged[int].connect(self.changeValue)
        # 将信号更新与控件控件setValue方法绑定，当信号更新时，控件更新
        self.c.updateBW[int].connect(self.wid.setValue)

        # 水平布局，自定义的wid控件将显示在底部
        hbox = QHBoxLayout()
        hbox.addWidget(self.wid)
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

        # 设置窗口
        self.setGeometry(300, 300, 390, 210)
        self.setWindowTitle('Burning widget')
        self.show()


    def changeValue(self, value):
        # 发送updateBW信号
        self.c.updateBW.emit(value)     

        # 重绘窗口，repaint update均可   
        #self.wid.repaint()
        self.wid.update()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())