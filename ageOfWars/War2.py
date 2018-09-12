import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QFrame, QScrollArea, QWidget, QVBoxLayout, QHBoxLayout, \
QScrollBar, QAbstractScrollArea
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QBrush, QPainterPath
from PyQt5.QtCore import Qt, QSize, QPoint, QEvent
import Config  # 配置
from AllPoint import board
import time


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
        # 窗口设置
        self.resize(QSize(Config.ConWindowWidth, Config.ConWindowHeight))
        self.setWindowTitle("原始战争")
    
    def paintEvent(self,event):
        '''重载绘图事件'''
        qp = QPainter(self)

        a = []
        for i in range(Config.ConWidth):
            for j in range(Config.ConHeight):
                
                qp.setPen(QColor(int(i*(256/Config.ConWidth)), int(j*(256/Config.ConHeight)), int(j*(256/Config.ConHeight))))
                qp.drawPoint(i, j)
                # 之后还需要#FFF置白, 先比对改变的点
        qp.end()

if __name__ == '__main__':
    app = QApplication([])
    war = War()
    war.show()
    sys.exit(app.exec_())