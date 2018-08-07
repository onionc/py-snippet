import sys
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout,  QLineEdit, QTextEdit

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        select='feedback'

        if select=='box':
            # 绝对定位
            for i in range(1,20):
                lb1=QLabel('(。・∀・)ノ',self)
                lb1.move(20*i,15*i)

            # 盒布局
            okButton = QPushButton("ok")
            cancelButton = QPushButton("cancel")

            hbox = QHBoxLayout()
            hbox.addStretch(1)
            hbox.addWidget(okButton)
            hbox.addWidget(cancelButton)
            
            vbox = QVBoxLayout()
            vbox.addStretch(1)
            vbox.addLayout(hbox)

            self.setLayout(vbox)

            self.setWindowTitle('绝对定位与盒布局')
        elif select=='grid':
            # 栅格布局
            grid = QGridLayout()
            self.setLayout(grid)
            names = ['Cls', 'Bck', '', 'Close',
                    '7', '8', '9', '/',
                    '4', '5', '6', '*',
                    '1', '2', '3', '-',
                    '0', '.', '=', '+']
            positions=[(i,j) for i in range(5) for j in range(4)]

            for position,name in zip(positions,names):
                if name=='':
                    continue
                button = QPushButton(name)
                grid.addWidget(button,*position)
                #print(position,*position)
            
            self.setWindowTitle('栅格布局')
        elif select=='feedback':
            title = QLabel('Title')
            author = QLabel('author')
            review = QLabel('review')

            titleEdit = QLineEdit()
            authorEdit = QLineEdit()
            reviewEdit = QTextEdit()

            grid = QGridLayout()
            grid.setSpacing(15)

            grid.addWidget(title,1,0)
            grid.addWidget(titleEdit,1,1)

            grid.addWidget(author,2,0)
            grid.addWidget(authorEdit,2,1)

            grid.addWidget(review,3,0)
            grid.addWidget(reviewEdit,3,1,5,1)

            self.setLayout(grid)
            
            self.setWindowTitle('基于栅格布局的反馈界面')
        # 窗口    
        self.setGeometry(300,300,500,300)
        
        self.show()
if __name__=='__main__':
    app=QApplication(sys.argv)
    ex=Example()
    sys.exit(app.exec_())