import sys
from PyQt5.QtWidgets import QPushButton, QWidget, QLineEdit, QApplication
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag

class Button(QPushButton):
    def __init__(self,title,parent):
        super().__init__(title,parent)
        self.setAcceptDrops(True)

    # 拖放到按钮上触发的事件
    def dragEnterEvent(self,e):
        if e.mimeData().hasFormat('text/plain'):
            e.accept()
        else:
            e.ignore()

    # 松开鼠标完成拖放时，把文字设置到button上
    def dropEvent(self,e):
        self.setText(e.mimeData().text())

    # 拖动
    def mouseMoveEvent(self,e):
        print('mouseMove')
        if e.buttons() != Qt.RightButton:
            return
        mimeData = QMimeData()
        drag=QDrag(self)
        drag.setMimeData(mimeData)
        #sdrag.setHotSpot(e.pos() - self.rect().topLeft())

        dropAction = drag.exec_(Qt.MoveAction)
        drag.exec_()
    
    # 点击
    def mousePressEvent(self,e):
        print('mousePress')
        #print('press-button ',e.button(),e.buttons())
        super().mousePressEvent(e)
        if e.button() == Qt.LeftButton:
            print('press')

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 简单拖放文字到button组件上
        edit=QLineEdit('',self)
        edit.setDragEnabled(True) # 文本框选定拖动
        edit.move(20,30)
        button=Button("BUTTON",self)
        button.move(190,30)
        
        # 拖放button组件
        self.setAcceptDrops(True)
        self.button = Button('Button',self)

        # 窗口
        self.setWindowTitle("drag")
        self.setGeometry(300,300,300,200)
    
    def dragEnterEvent(self,e):
        e.accept()
    
    def dropEvent(self,e):
        position=e.pos()
        self.button.move(position)

        e.setDropAction(Qt.MoveAction)
        e.accept()

if __name__ == '__main__':
    app=QApplication(sys.argv)
    ex=Example()
    ex.show()
    sys.exit(app.exec_())