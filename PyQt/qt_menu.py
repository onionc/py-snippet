import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, qApp, QMenu, QTextEdit
from PyQt5.QtGui import QIcon

class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 状态栏
        self.statusbar=self.statusBar()
        self.statusbar.showMessage('loading...')
        
        # 动作
        exitAct = QAction(QIcon(sys.path[0]+'/music.png'),'&Exit',self)
        exitAct.setShortcut('Ctrl+1')
        exitAct.setStatusTip('load failed')
        exitAct.triggered.connect(qApp.quit)

        # 菜单
        menubar = self.menuBar()
        exitMenu = menubar.addMenu('&Exit')
        exitMenu.addAction(exitAct)

        # 多级菜单和动作
        ## 菜单栏加一项
        fileMenu = menubar.addMenu('File')
        ## 添加Add动作
        addAct = QAction('Add',self)
        fileMenu.addAction(addAct)
        ## 添加'save as'动作和'save'菜单，并将'Save as'动作加到'Save'菜单上
        saveAsAct = QAction('Save as',self)
        saveMenu = QMenu('save',self)
        saveMenu.addAction(saveAsAct)
        fileMenu.addMenu(saveMenu)
        
        # 勾选菜单
        viewMenu = menubar.addMenu('View')
        viewStatAct = QAction('View statusbar',self,checkable=True)
        viewStatAct.setStatusTip('..check me.')
        viewStatAct.setChecked(True)
        viewStatAct.triggered.connect(self.toggleMenu)
        viewMenu.addAction(viewStatAct)

        # 工具栏,用到了上面的exitAct
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAct)

        # 文本框
        textEdit = QTextEdit()
        self.setCentralWidget(textEdit)

        # 窗口
        #self.setGeometry(300,300,250,150)
        self.setWindowTitle('原始人')
        self.show()

    # 勾选（取消勾选）动作处理
    def toggleMenu(self,state):
        if state:
            self.statusbar.show()
        else:
            self.statusbar.hide()

    # 右键菜单事件
    def contextMenuEvent(self,event):
        #print('right')
        cmenu = QMenu(self)
        act1 = cmenu.addAction('原')
        act2 = cmenu.addAction('生')
        act3 = cmenu.addAction('右')
        act4 = cmenu.addAction('键')
        quitAct = cmenu.addAction('X')
        action = cmenu.exec_(self.mapToGlobal(event.pos()))

        if action==quitAct:
            #print(action,quitAct)
            qApp.quit()
        else:
            self.statusbar.show()
            self.statusbar.showMessage("缘,妙不可言")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex=Example()
    sys.exit(app.exec_())