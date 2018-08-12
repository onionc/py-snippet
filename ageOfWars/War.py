import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QFrame, QScrollArea, QWidget, QVBoxLayout, QHBoxLayout, \
QScrollBar, QAbstractScrollArea
from PyQt5.QtCore import QSize, Qt, QEvent, QPoint
from PyQt5.QtGui import QPixmap

class War(QMainWindow):
    '''游戏主类'''
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.lbl = QLabel(self)
        self.qpix=QPixmap(sys.path[0]+'/resource/57001_one_punch_man.jpg').scaledToHeight(480)
        self.lbl.setGeometry(self.qpix.rect())
        self.lbl.setPixmap(self.qpix)
        print(self.lbl)
        # 添加滚动条，并添加组件
        scrollArea = QScrollArea2(self)
        scrollArea.setWidgetResizable(True)
        #scrollArea.setBackgroundRole(QPalette::Dark);
        scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff) # 隐藏滚动条
        scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scrollArea.setWidget(self.lbl)
        scrollArea.resize(QSize(720,480))
  
        # 窗口设置
        self.resize(QSize(720,480))
        self.setWindowTitle("原始战争")

        #self.scroll(400,200)
        #self.update()

class QScrollArea2(QScrollArea):
    def __init__(self, parent):
        super().__init__(parent)

        self.n=0.8
        self.m_prev = QPoint()
        self.diff = QPoint()
        self.prev_diff = QPoint(0, 0)
        self.l = None


    def setWidget(self, w):
        super().setWidget(w)
        self.l=w
        self.l.installEventFilter(self)
        
    def eventFilter(self,obj,evt):
        #print(QScrollArea.widget(self),obj)
        if(obj!=self.l):
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
            print('diff x :',self.diff.x())
            self.m_prev = pt
            
            print(self.horizontalScrollBar().value()+self.diff.x()*self.n,'--')
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value()+self.diff.x()*self.n)
            #horizontalScrollBar().setValue(horizontalScrollBar().value()+self.diff.x()*self.n);
            # verticalScrollBar()->setValue(verticalScrollBar()->value()+diff.y()*n);
            self.prev_diff=self.diff;
            return True
        return QScrollArea.eventFilter(self,obj, evt)

   
if __name__ == '__main__':
    app = QApplication([])
    war = War()
    war.show()
    sys.exit(app.exec_())