import sys
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QLineEdit, QHBoxLayout, QFrame, QSplitter, QStyleFactory, QComboBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # QPixmap 上节已体验过，pass
        
        # 行编辑
        self.lbl=QLabel(self)
        self.lbl.move(180,40)
        qle=QLineEdit(self)
        qle.move(20,40)
        qle.textChanged[str].connect(self.onChanged)
        
        # QSplitter 拖拽分割
        hbox = QHBoxLayout()

        topLeft = QFrame(self)
        topLeft.setFrameShape(QFrame.StyledPanel)
        topRight = QFrame(self)
        topRight.setFrameShape(QFrame.StyledPanel)
        bottom = QFrame(self)
        bottom.setFrameShape(QFrame.StyledPanel)

        splitter1 = QSplitter(Qt.Horizontal)
        splitter1.addWidget(topLeft)
        splitter1.addWidget(topRight)

        splitter2 = QSplitter(Qt.Vertical)
        splitter2.addWidget(splitter1)
        splitter2.addWidget(bottom)

        hbox.addWidget(splitter2)
        self.setLayout(hbox)

        # 下拉框
        combo = QComboBox(self)
        for i in range(1,6):
            combo.addItem(str(i))
        combo.move(20,150)
        
        self.comLb = QLabel("",self)
        self.comLb.move(130,157)

        combo.activated[str].connect(self.onActivated)

        # 窗口
        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('QLineEdit')
        self.show()

    # 行编辑改变
    def onChanged(self,text):
        self.lbl.setText(text)
        self.lbl.adjustSize()

    # 下拉触发
    def onActivated(self,text):
        self.comLb.setText(text)
        self.comLb.adjustSize()

if __name__ == '__main__':
    app=QApplication(sys.argv)
    ex=Example()
    sys.exit(app.exec_())