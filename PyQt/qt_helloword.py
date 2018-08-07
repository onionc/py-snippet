import sys
from PyQt5.QtWidgets import QApplication, QWidget, QToolTip, QPushButton, QMessageBox, QDesktopWidget
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QCoreApplication

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        # location and size 
        self.setGeometry(300,300,300,300)
        
        # title
        self.setWindowTitle('Icon')
        
        # icon
        self.setWindowIcon(QIcon(sys.path[0]+'/music.png'))
        
        # 提示消息字体
        QToolTip.setFont(QFont('Georgia',10))

        # 提示框
        self.setToolTip('this is <br/><i>python</i> and <i>pyqt5</i><hr/> program')

        # 按钮以及提示框
        btn=QPushButton('退出',self)
        # 退出事件
        btn.clicked.connect(QCoreApplication.instance().quit)
        btn.setToolTip('quick, quick click')
        #btn.resize(btn.sizeHint())
        btn.move(50,50)

        self.center()
        self.show()
        
    # 关闭事件
    def closeEvent(self,event):
        print('close')
        reply = QMessageBox.question(self,"answer","To be or not to be?",QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            #print(QMessageBox.Yes)
            event.accept()
        else:
            reply = QMessageBox.question(self,'😕','are you sure? must quit',QMessageBox.Yes, QMessageBox.Yes)
            #event.ignore()
            event.accept() 
            
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        print(cp)
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())