import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLCDNumber, QSlider, QVBoxLayout, QApplication, QGridLayout, QLabel

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        # 基础
        lcd = QLCDNumber(self)
        sld = QSlider(Qt.Horizontal,self)
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(lcd)
        vbox.addWidget(sld)
        self.setLayout(vbox)
        sld.valueChanged.connect(lcd.display)

        # 添加一个label组件，用来显示（通过鼠标移动事件对象产生的）坐标
        grid = QGridLayout()
        grid.setSpacing(10)
        x=0
        y=0
        self.text="({0},{1})".format(x,y)
        self.label=QLabel(self.text,self)
        grid.addWidget(self.label,0,0,Qt.AlignTop)
        ## 开启鼠标追踪
        self.setMouseTracking(True)
        self.setLayout(grid)
       
        #窗口
        self.setGeometry(300,300,250,350)
        self.setWindowTitle('Signal and slot')
        self.show()
    
    # 重构事件处理器，按键事件
    def keyPressEvent(self,e):
        # print(e.key())
        # wasd 87 65 83 68
        if e.key()==Qt.Key_Escape:
            self.close()

    # 鼠标移动事件
    def mouseMoveEvent(self,e):
        x=e.x()
        y=e.y()
        text="({0},{1})".format(x,y)
        self.label.setText(text)
    
    def buttonClicked(self):
        sender = self.sender()
        self.statusBar().showMessage(sender.text()+"was pressed")

if __name__=='__main__':
    app=QApplication(sys.argv)
    ex=Example()
    sys.exit(app.exec_())