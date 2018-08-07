import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QFileDialog, QTextEdit
from PyQt5.QtGui import QIcon

class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 选择文件
        self.textEdit = QTextEdit() # 文本框
        self.setCentralWidget(self.textEdit) #置中的文本编辑框
        self.statusBar() # 状态栏
        ## 菜单action
        openFileAct = QAction('open',self)
        openFileAct.setShortcut('Ctrl+Q')
        openFileAct.setStatusTip("open new File")
        openFileAct.triggered.connect(self.showFileDialog)
        ## 菜单
        menubar = self.menuBar()
        fileMenu = menubar.addMenu("&File")
        fileMenu.addAction(openFileAct)

        # 窗口
        self.setGeometry(300,300,500,400)
        self.setWindowTitle('对话框')
        self.show()

    # 文件对话框
    def showFileDialog(self):
        fname = QFileDialog.getOpenFileName(self,"open file")
        if fname[0]:
            f=open(fname[0],'r',encoding="UTF-8")

            with f:
                data = f.read()
                self.textEdit.setText(data)

if __name__ == '__main__':
    app=QApplication(sys.argv)
    ex=Example()
    sys.exit(app.exec_())