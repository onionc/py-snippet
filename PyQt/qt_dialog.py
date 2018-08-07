import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QInputDialog, QApplication, QFrame, QColorDialog, QHBoxLayout, QSizePolicy, QLabel, QFontDialog
from PyQt5.QtGui import QColor

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 输入文字
        self.btn = QPushButton('NAME',self)
        self.btn.move(20,20)
        self.btn.clicked.connect(self.showDialog)
        ## 文本框
        self.le=QLineEdit(self)
        self.le.move(130,22)

        # 选取颜色
        col = QColor(0,0,0)
        self.btn=QPushButton('Color',self)
        self.btn.move(20,60)
        self.btn.clicked.connect(self.showColorWheelDialog)
        ## QFrame
        self.frm = QFrame(self)
        self.frm.setStyleSheet("QWidget{background-color:%s}" % col.name())
        self.frm.setGeometry(130,60,100,100)

        # 选择字体
        btn=QPushButton("Font",self)
        btn.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        btn.move(20,175)
        btn.clicked.connect(self.showFontDialog)

        self.lbl=QLabel("Remembrance of things past is <br/>not necessarily the remembrance of things as <br/>they were. <br/> --Marcel Proust",self)
        self.lbl.setGeometry(130,160,300,100)

        # 窗口
        self.setGeometry(300,300,500,400)
        self.setWindowTitle('对话框')
        self.show()

    # 文本对话框
    def showDialog(self):
        text,ok = QInputDialog.getText(self,'input dialog','enter your name:')
        if ok:
            self.le.setText(str(text))
    
    # 颜色盘对话框
    def showColorWheelDialog(self):
        col = QColorDialog.getColor()
        if col.isValid():
            # 用 background也可以
            self.frm.setStyleSheet("background:{0}".format(col.name()))
            # 试着给字体加颜色，bingo!
            self.lbl.setStyleSheet("color:{0}".format(col.name()))
            self.le.setStyleSheet("color:{0}".format(col.name()))
    # 字体对话框
    def showFontDialog(self):
        font,ok=QFontDialog.getFont()
        if ok:
            self.lbl.setFont(font)
            self.le.setFont(font)


if __name__ == '__main__':
    app=QApplication(sys.argv)
    ex=Example()
    sys.exit(app.exec_())