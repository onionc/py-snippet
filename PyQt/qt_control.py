import sys
from PyQt5.QtWidgets import QWidget, QApplication, QCheckBox, QPushButton, QFrame, QSlider, QLabel, QProgressBar, QHBoxLayout, QCalendarWidget
from PyQt5.QtCore import Qt, QSize, QBasicTimer, QDate
from PyQt5.QtGui import QColor, QPixmap, QIcon

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        
        # 选择框 QCheckBox
        cb = QCheckBox("show title",self)
        cb.move(20,20)
        #cb.toggle()
        cb.stateChanged.connect(self.changeTitle)
        
        # 切换按钮
        self.col = QColor(0,0,0)
        redb=QPushButton('RED',self)
        redb.setCheckable(True)
        redb.move(20,40)
        redb.clicked[bool].connect(self.setColor) # 将点击信号转换为布尔值，并与函数关联起来

        greenb=QPushButton('GREEN',self)
        greenb.setCheckable(True)
        greenb.move(20,60)
        greenb.clicked[bool].connect(self.setColor)

        blueb=QPushButton('BLUE',self)
        blueb.setCheckable(True)
        blueb.move(20,80)
        blueb.clicked[bool].connect(self.setColor)

        self.square = QFrame(self)
        self.square.setGeometry(150,20,100,100)
        self.square.setStyleSheet("QFrame{background-color:%s}" % self.col.name())
        
        # 滑块 QSlider
        sld = QSlider(Qt.Horizontal,self)
        sld.setFocusPolicy(19)
        sld.setGeometry(20,160,100,30)
        sld.valueChanged[int].connect(self.changeSliderValue)

        self.label = QLabel(self)
        qpix=QPixmap(sys.path[0]+'/music2.png').scaled(QSize(30,30))
        self.label.setPixmap(qpix)
        self.label.setGeometry(150,160,30,30)

        self.labelText = QLabel(self)
        self.labelText.setGeometry(190,160,13,10)

        # 进度条
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(120,200,200,25)
        
        self.btn = QPushButton('Start',self)
        self.btn.move(20,200)
        self.btn.clicked.connect(self.doAction)

        self.timer = QBasicTimer()
        self.step=0

        # 日历
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        
        cal=QCalendarWidget(self)
        cal.setGridVisible(True)
        cal.clicked[QDate].connect(self.showDate)
        hbox.addWidget(cal)
        
        self.lbl=QLabel(self)
        date=cal.selectedDate()
        self.lbl.setText(date.toString())
        hbox.addWidget(self.lbl)

        self.setLayout(hbox)

        # 窗口
        self.setGeometry(300,300,500,400)
        self.setWindowTitle('Control')
        self.show()

    # 通过checkbox改变标题
    def changeTitle(self,state):
        if state==Qt.Checked:
            self.setWindowTitle('QChekcBox')
        else:
            self.setWindowTitle('Control')

    # 通过button改变颜色
    def setColor(self,preesed):
        source=self.sender() # 找到事件信号发送者
        
        if preesed:
            val=255
        else:
            val=0
        
        if source.text() == "RED":
            self.col.setRed(val)
        elif source.text() == 'GREEN':
            self.col.setGreen(val)
        else:
            self.col.setBlue(val)

        self.square.setStyleSheet("QFrame{background-color:%s}" % self.col.name())

    # 通过QSlider滑动改变
    def changeSliderValue(self,value):
        # 置label为value
        self.labelText.setText(str(value))
        if value==0:
            self.label.setPixmap(QPixmap(sys.path[0]+'/music2.png').scaled(QSize(30,30)))
        elif value>0 and value <=30:
            self.label.setPixmap(QPixmap(sys.path[0]+'/music.png').scaled(QSize(30,30)))
        elif value>30 and value <80:
            self.label.setPixmap(QPixmap(sys.path[0]+'/music.png').scaled(QSize(30,30)))
        else:
            self.label.setPixmap(QPixmap(sys.path[0]+'/music.png').scaled(QSize(30,30)))
    
    # QBasicTimer的start()方法触发的事件，重载
    def timerEvent(self,e):
        if self.step>=100:
            self.timer.stop()
            self.btn.setText("Finished")
            return
        self.step=self.step+1
        self.pbar.setValue(self.step)
    
    # 按钮信号，控制开始/停止
    def doAction(self):
        if self.timer.isActive():
            self.timer.stop()
            self.btn.setText("Start")
        else:
            self.timer.start(100,self)
            self.btn.setText("Stop")
        
    # 日期
    def showDate(self,date):
        self.lbl.setText(date.toString())

if __name__ == '__main__':
    app=QApplication(sys.argv)
    ex=Example()
    sys.exit(app.exec_())