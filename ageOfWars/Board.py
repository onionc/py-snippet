from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap
from 
class Board(QWidget):
    '''游戏界面类'''
    def __init__(self, parent):
        super().__init__(parent)
        self.initBoard()

    def initBoard(self):
        print("board comming soon.")