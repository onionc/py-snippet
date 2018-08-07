import sys
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication

# 自定义closeApp信号
class Communicate(QObject):
    closeApp = pyqtSignal()

class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 事件发送
        btn1 = QPushButton("Button 1",self)
        btn1.move(30,50)
        btn2 = QPushButton("Button 2",self)
        btn2.move(150,50)
        btn1.clicked.connect(self.buttonClicked)
        btn2.clicked.connect(self.buttonClicked)
        ## 显示状态栏
        self.statusBar()

        # 自定义信号发送
        self.c = Communicate()
        self.c.closeApp.connect(self.close)
        
        #窗口
        self.setGeometry(300,300,250,350)
        self.setWindowTitle('Signal and slot')
        self.show()

    # slot，事件发送：发送者为button,接收者为状态栏statusBar
    def buttonClicked(self):
        sender = self.sender()
        self.statusBar().showMessage(sender.text()+" was pressed")

    # 发送closeApp信号
    def mousePressEvent(self,event):
        self.c.closeApp.emit()

if __name__=='__main__':
    app=QApplication(sys.argv)
    ex=Example()
    sys.exit(app.exec_())