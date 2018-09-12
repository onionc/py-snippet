import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QFrame, QScrollArea, QWidget, QVBoxLayout, QHBoxLayout, \
QScrollBar, QAbstractScrollArea
from PyQt5.QtCore import QSize, Qt, QEvent, QPoint
from PyQt5.QtGui import QPixmap, QPainter
import Config  # 配置

class War(QMainWindow):
    '''游戏主类'''
    def __init__(self):
        super().__init__()
    
        self.currentLeftX = 0
        self.currentRightX = self.getRightX(self.currentLeftX)
        
        self.initUI()
    
    def getRightX(self, leftX):
        '''通过左侧X（绘制的左边）得到右侧X'''
        rightX = leftX + Config.ConWindowWidth
        if rightX > Config.ConWidth:
            rightX = Config.ConWidth
            leftX = self.rightX-Config.ConWindowWidth
        
        return rightX

    def initUI(self):

        ''' 
        添加图片
        self.lbl = QLabel(self)
        self.qpix=QPixmap(sys.path[0]+'/resource/57001_one_punch_man.jpg').scaledToHeight(480)
        self.lbl.setGeometry(self.qpix.rect())
        self.lbl.setPixmap(self.qpix)
        '''
        self.lbl = QLabel(self)
        self.lbl.setGeometry(0, 0, 100, 100)

        # 添加滚动条，并添加组件
        scrollArea = ScrollArea(self)
        scrollArea.setWidgetResizable(True)
        # scrollArea.setBackgroundRole(QPalette::Dark);
        scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 隐藏滚动条
        scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scrollArea.setWidget(self.lbl)
        scrollArea.resize(QSize(720, 480))
  
        # 窗口设置
        self.resize(QSize(720, 480))
        self.setWindowTitle("原始战争")

        # self.scroll(400,200)
        # self.update()

    def paintEvent(self, event):
        '''重载绘图事件'''
        qp = QPainter()
        qp.begin(self)

        # 文字
        self.text = "何须剑道争锋？千人指，万人封，可问江湖鼎峰；三尺秋水尘不染，天下无双。何须剑道争锋？千人指，万人封，可问江湖鼎峰；三尺秋水尘不染，天下无双。何须剑道争锋？千人指，万人封，可问江湖鼎峰；三尺秋水尘不染，天下无双。何须剑道争锋？千人指，万人封，可问江湖鼎峰；三尺秋水尘不染，天下无双。何须剑道争锋？千人指，万人封，可问江湖鼎峰；三尺秋水尘不染，天下无双。何须剑道争锋？千人指，万人封，可问江湖鼎峰；三尺秋水尘不染，天下无双。11"
        
        self.lbl.setText(self.text)
        qp.end()


class ScrollArea(QScrollArea):
    '''重载滚动条类'''
    def __init__(self, parent):
        super().__init__(parent)

        self.n=0.8
        self.m_prev = QPoint()
        self.diff = QPoint()
        self.prev_diff = QPoint(0, 0)
        self.widget = None


    def setWidget(self, w):
        '''设置区域部件时，对象赋值'''
        super().setWidget(w)
        self.widget=w
        self.widget.installEventFilter(self)
        
    def eventFilter(self,obj,evt):
        '''事件过滤'''
        #print(QScrollArea.widget(self),obj)
        if(obj!=self.widget):
            return super().eventFilter(obj,evt)
        
        if(evt.type()==QEvent.MouseButtonPress):
            self.m_prev = evt.pos()
            self.prev_diff.setX(0)
            self.prev_diff.setY(0)

        # 鼠标移动
        # MouseMove为鼠标拖动效果，鼠标滑动是ToolTip
        if(evt.type()==QEvent.MouseMove):  
            #print(evt.pos())
            pt = evt.pos()
            self.diff = pt-self.m_prev-self.prev_diff*self.n
            self.diff = -1*self.diff
            # print('diff x :',self.diff.x())
            self.m_prev = pt
            
            # print(self.horizontalScrollBar().value()+self.diff.x()*self.n,'--')
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value()+self.diff.x()*self.n)
            
            self.prev_diff = self.diff
            return True
        return QScrollArea.eventFilter(self, obj, evt)


if __name__ == '__main__':
    app = QApplication([])
    war = War()
    war.show()
    sys.exit(app.exec_())