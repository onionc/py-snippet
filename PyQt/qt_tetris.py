import sys
import random
from PyQt5.QtWidgets import QMainWindow, QFrame, QApplication, QDesktopWidget, QMessageBox, qApp
from PyQt5.QtCore import Qt, pyqtSignal, QBasicTimer
from PyQt5.QtGui import QPainter, QColor


class Tetris(QMainWindow):
    '''创建游戏'''
    
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        '''初始应用程序UI'''
        # 调用主要逻辑处理
        self.tboard = Board(self)
        self.setCentralWidget(self.tboard)

        # 将状态栏组件显示信息方法和Board信号msg2StatusBar绑定
        self.tboard.msg2StatusBar[str].connect(self.statusBar().showMessage)  # msg2Statusbar 信号

        # 开始游戏
        self.tboard.start()
        
        # 窗口位置及窗口显示
        self.resize(180, 380)
        self.center()
        self.setWindowTitle("俄罗斯方块")
        self.show()

    def center(self):
        '''窗口居中'''
        # class QDesktopWidget 可获取系统屏幕信息
        # screenGeometry() 返回QRect格式屏幕大小 eg. PyQt5.QtCore.QRect(0, 0, 1366, 768)
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move( (screen.width()-size.width())/2, (screen.height()-size.height())/2 )


class Board(QFrame):
    '''主要逻辑'''

    # 自定义信号，看名称可以猜出和状态栏有关
    msg2StatusBar = pyqtSignal(str)

    # 一些配置,界面宽高（按每个小方块分），初始速度
    BoardWidth = 10
    BoardHeight = 22
    BaseSpeed = 300

    # 每次升级提高速度
    SpeedUp = 50

    def __init__(self, parent):
        super().__init__(parent)
        self.initBoard()

    def initBoard(self):
        '''初始界面（面板）'''
        # 计时器创建游戏循环
        self.timer = QBasicTimer()
        # 设置等待，为True则等到下一个timer循环激活
        self.isWaitingAfterLine = False

        self.curX = 0
        self.curY = 0
        # 消除的行数，即总成绩
        self.score = 0
        # self.board列表存储所有的砖块，值为Bricks定义的砖块值
        self.board = []
        # 等级
        self.level = 1
        # 速度
        self.speed = Board.BaseSpeed
        # 部件聚焦策略 StrongFocus: TabFocus | ClickFocus. 接受tab和单击
        self.setFocusPolicy(Qt.StrongFocus)
        
        self.isStarted = False
        self.isPaused = False
        self.clearBoard()

    def start(self):
        '''开始游戏'''
        
        # 暂停
        if self.isPaused:
            return
        
        self.isStarted = True
        self.isWaitingAfterLine = False
        self.score = 0
        self.clearBoard()

        # 发送msg2StatusBar信号以更新(消除的行数(成绩))到状态栏
        self.msg2StatusBar.emit(str(self.score))

        # 创建方块
        self.newPiece()

        self.timer.start(self.speed, self)
        
    def clearBoard(self):
        '''从界面清除形状'''

        # 看出来用Noshape即0充满了self.board列表
        for i in range(Board.BoardHeight * Board.BoardWidth):
            self.board.append(Bricks.NoShape)

    def newPiece(self):
        '''创建一个新砖块'''

        self.curPiece = Shape()
        self.curPiece.setRandomShape()
        self.curX = Board.BoardWidth//2 + 1
        self.curY = Board.BoardHeight-1 + self.curPiece.minY()

        # 不能移动时则游戏结束
        if not self.tryMove(self.curPiece,self.curX,self.curY):
            self.curPiece.setShape(Bricks.NoShape)
            self.timer.stop()
            self.isStarted = False
            self.msg2StatusBar.emit('Game Over')  
            # 增加结束界面
            self.gameOver()

    def tryMove(self,newPiece,newX,newY):
        ''' 尝试移动砖块，不可移动返回False, GameOver '''
        for i in range(4):
            x = newX + newPiece.x(i)
            y = newY - newPiece.y(i)

            # 超边界
            if x<0 or x>=Board.BoardWidth or y<0 or y>=Board.BoardHeight:
                return False
            
            # 不为空
            if self.shapeAt(x, y) != Bricks.NoShape:
                return False
        
        self.curPiece = newPiece
        self.curX = newX
        self.curY = newY
        self.update()

        return True

    def shapeAt(self,x,y):
        '''界面的[x,y]位置小方块的砖块形状'''
        '''比如L在界面里可能为这样：
            0 0 0 0 0 0 6 0 0 0
            0 0 0 0 0 0 6 0 0 0
            0 0 0 0 0 0 6 6 0 0 
        '''
        return self.board[y*Board.BoardWidth+x]
    
    def setShapeAt(self,x,y,shape):
        ''' 在界面设置砖块的位置 '''
        self.board[y*Board.BoardWidth+x]=shape
    
    def squareWidth(self):
        '''返回一个小方块的宽'''
        return self.contentsRect().width() // Board.BoardWidth

    def squareHeight(self):
        '''返回一个小方块的高'''
        return self.contentsRect().height() // Board.BoardHeight

    def paintEvent(self,event):
        '''在游戏中绘制砖块！'''

        painter = QPainter(self)
        rect = self.contentsRect()  # 返回部件边距内区域
        
        '''
         rect.bottom()界面内高，减去小方块的规定高*每个小方块实际高，为界面顶部。
         界面顶boardTop则为可以下砖块的地方
        '''
        boardTop = rect.bottom() - Board.BoardHeight * self.squareHeight()
        
        # 遍历界面宽高，画已经存在的小方块
        for i in range(Board.BoardHeight):
            for j in range(Board.BoardWidth):
                
                # 每个位置
                shape = self.shapeAt(j, Board.BoardHeight-i-1)

                if shape != Bricks.NoShape:
                    
                    self.drawSquare(
                        painter,
                        rect.left()+j*self.squareWidth(),
                        boardTop+i*self.squareHeight(),
                        shape
                    )
        
        # 正在下落的新砖块，绘制4小方块
        if self.curPiece.shape() != Bricks.NoShape:
            for i in range(4):
                x=self.curX+self.curPiece.x(i)
                y=self.curY-self.curPiece.y(i)
                self.drawSquare(
                    painter,
                    rect.left()+x*self.squareWidth(),
                    boardTop+(Board.BoardHeight-y-1)*self.squareHeight(),
                    self.curPiece.shape()
                )

    def drawSquare(self,painter,x,y,shape):
        '''绘制每个砖块（形状）的正方形, 核心绘制'''
        colorTable = [0x000000, 0xCC6666, 0x66CC66, 0x6666CC,
                      0xCCCC66, 0xCC66CC, 0x66CCCC, 0xDAAA00]

        # 画矩形
        color = QColor(colorTable[shape])
        painter.fillRect(x + 1, y + 1, self.squareWidth() - 2, 
            self.squareHeight() - 2, color)

        # 用亮的/暗的线画四边，光亮阴影效果
        painter.setPen(color.lighter())
        painter.drawLine(x, y + self.squareHeight() - 1, x, y)  # 左
        painter.drawLine(x, y, x + self.squareWidth() - 1, y)  # 上

        painter.setPen(color.darker())
        painter.drawLine(x + 1, y + self.squareHeight() - 1, x + self.squareWidth() - 1, y + self.squareHeight() - 1)  # 下
        painter.drawLine(x + self.squareWidth() - 1, y + self.squareHeight() - 1, x + self.squareWidth() - 1, y + 1)  # 右

    def oneLineDown(self):
        '''砖块下落一行'''
        if not self.tryMove(self.curPiece,self.curX,self.curY-1):
            self.pieceDropped()
    
    def timerEvent(self,event):
        '''定时器事件'''
        # print(event.timerId(),self.timer.timerId())
        if event.timerId() == self.timer.timerId():
            if self.isWaitingAfterLine:
                self.isWaitingAfterLine=False
                self.newPiece()
            else:
                self.oneLineDown()
        else:
            super(Board, self).timeEvent(event)


    def keyPressEvent(self, event):
        '''处理按键事件'''
        if not self.isStarted or self.curPiece.shape() == Bricks.NoShape:
            super(Board, self).keyPressEvent(event)
            return 
        
        key = event.key()

        if key==Qt.Key_P:
            self.pause()
            return
        if self.isPaused:
            return
        elif key==Qt.Key_Left:
            self.tryMove(self.curPiece,self.curX-1,self.curY)
        elif key==Qt.Key_Right:
            self.tryMove(self.curPiece,self.curX+1,self.curY)
        elif key==Qt.Key_Down:
            self.tryMove(self.curPiece.rotateRight(),self.curX,self.curY)
        elif key==Qt.Key_Up:
            self.tryMove(self.curPiece.rotateLeft(),self.curX,self.curY)
        elif key==Qt.Key_Space:
            self.dropDown()
        elif key==Qt.Key_D:
            self.oneLineDown()
        else:
            super(Board, self).keyPressEvent(event)
    
    def dropDown(self):
        '''下降一个砖块'''

        newY = self.curY
        while newY > 0:
            if not self.tryMove(self.curPiece, self.curX, newY - 1):
                break
            newY -= 1
        self.pieceDropped()

    def pause(self):
        '''暂停游戏'''

        if not self.isStarted:
            return

        self.isPaused = not self.isPaused

        # 如果可以暂停，则事件停止，并发送文字到状态栏
        if self.isPaused:
            self.timer.stop()
            self.msg2StatusBar.emit("暂停中，按p键恢复游戏")

        else:
            self.timer.start(self.speed, self)
            self.msg2StatusBar.emit(str(self.score))

        self.update()
    
    def pieceDropped(self):
        '''砖块下降后，检测满行移除和检测是否创建新砖块'''

        for i in range(4):

            x = self.curX + self.curPiece.x(i)
            y = self.curY - self.curPiece.y(i)
            self.setShapeAt(x, y, self.curPiece.shape())

        self.removeFullLines()

        # 满行消除之后则会等待, 在下一次的timer事件生成newPiece()
        if not self.isWaitingAfterLine:
            self.newPiece()

    def removeFullLines(self):
        '''从界面移除满行'''

        numFullLines = 0
        rowsToRemove = []

        # 找所有满行
        for i in range(Board.BoardHeight):
            line=[self.shapeAt(j, i) for j in range(Board.BoardWidth)]
            if Bricks.NoShape not in line:
                rowsToRemove.append(i)
        
        # 反转，因为之前代码是从0（底部）行往上获取的，所以先消除上层避免浮空
        rowsToRemove.reverse()

        for m in rowsToRemove:

            for k in range(m, Board.BoardHeight):
                for l in range(Board.BoardWidth):
                        self.setShapeAt(l, k, self.shapeAt(l, k + 1))

        numFullLines = numFullLines + len(rowsToRemove)

        # 有删除行则更新成绩
        if numFullLines > 0:
            
            # 单次成绩，消除多行成绩翻幂倍
            singleScore=min(4,numFullLines)
            singleScore**=singleScore

            # 更新成绩
            self.score = self.score + singleScore
            self.msg2StatusBar.emit(str(self.score))
            
            self.isWaitingAfterLine = True # 等待
            self.curPiece.setShape(Bricks.NoShape) # 设置当前形状为空，已落地，无用
            self.upgrade() # 升级
            self.update() # 更新窗口

    def upgrade(self):
        '''升级处理，提升难度'''
        # 当前等级
        self.level=self.score//10+1
        # 简单加速度处理
        speed = max(10, Board.BaseSpeed-(self.level-1)*Board.SpeedUp) # level-1 代表1级为初始速度
        self.speed = speed
        # 设置timer循环速度
        self.timer.start(self.speed, self)
        
    def gameOver(self):
        '''结束界面'''
        reply=QMessageBox.information(self, "游戏结束", "总分数{0}\n是否再次开始".format(self.score), QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            self.initBoard()
            self.start()
        else:
            qApp.quit()

class Bricks(object):
    '''所有砖块'''

    NoShape = 0
    ZShape = 1
    SShape = 2
    LineShape = 3
    TShape = 4
    SquareShape = 5
    LShape = 6
    MirroredLshape = 7 # 反向L

class Shape(object):
    '''形状（砖块）代码'''
    
    # 砖块坐标
    coordsTable = (
        ((0, 0),     (0, 0),     (0, 0),     (0, 0)),
        ((0, -1),    (0, 0),     (-1, 0),    (-1, 1)),
        ((0, -1),    (0, 0),     (1, 0),     (1, 1)),
        ((0, -1),    (0, 0),     (0, 1),     (0, 2)),
        ((-1, 0),    (0, 0),     (1, 0),     (0, 1)),
        ((0, 0),     (1, 0),     (0, 1),     (1, 1)),
        ((-1, -1),   (0, -1),    (0, 0),     (0, 1)),
        ((1, -1),    (0, -1),    (0, 0),     (0, 1))
    )

    def __init__(self):
        
        self.coords = [[0,0] for i in range(4)]
        self.pieceShape = Bricks.NoShape
        self.setShape(Bricks.NoShape)

    def shape(self):
        '''返回形状'''
        return self.pieceShape

    def setShape(self,shape):
        '''设置形状'''
        table = Shape.coordsTable[shape]
        for i in range(4):
            for j in range(2):
                self.coords[i][j]=table[i][j]
        
        self.pieceShape = shape

    def setRandomShape(self):
        '''选择一个随机形状'''
        self.setShape(random.randint(1,7))

    def x(self,index):
        '''返回x坐标'''
        return self.coords[index][0]

    def y(self,index):
        '''返回y坐标'''
        return self.coords[index][1]

    def setX(self,index,x):
        '''设置x坐标'''
        self.coords[index][0]=x

    def setY(self,index,y):
        '''设置y坐标'''
        self.coords[index][1]=y
    
    def minX(self):
        '''返回最小的x'''
        m = self.coords[0][0]
        for i in range(4):
            m = min(m, self.coords[i][0])
        return m
    
    def maxX(self):
        '''返回最大的x'''
        m = self.coords[0][0]
        for i in range(4):
            m = max(m, self.coords[i][0])
        return m

    def minY(self):
        '''返回最小的y'''
        m = self.coords[0][1]
        for i in range(4):
            m = min(m, self.coords[i][1])
        return m

    def maxY(self):
        '''返回最大的y'''
        m = self.coords[0][1]
        for i in range(4):
            m = max(m, self.coords[i][1])
        return m

    def rotateLeft(self):
        '''左旋转砖块'''
        
        # 方块不做旋转
        if self.pieceShape == Bricks.SquareShape:
            return self
        
        result = Shape()
        result.pieceShape = self.pieceShape

        for i in range(4):
            result.setX(i,-self.y(i))
            result.setY(i,self.x(i))

        return result

    def rotateRight(self):
        '''右旋转砖块'''
        
        if self.pieceShape == Bricks.SquareShape:
            return self
        
        result = Shape()
        result.pieceShape = self.pieceShape

        for i in range(4):
            result.setX(i,self.y(i))
            result.setY(i,-self.x(i))
        
        return result

if __name__ == '__main__':
    app=QApplication([])
    tetris = Tetris()
    sys.exit(app.exec_())

