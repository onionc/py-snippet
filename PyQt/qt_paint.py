import sys, random
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QBrush, QPainterPath
from PyQt5.QtCore import Qt

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 文本涂鸦
        self.text="何须剑道争锋？\n千人指，万人封，可问江湖鼎峰；\n三尺秋水尘不染，天下无双。"

        # 窗口
        self.setGeometry(300,200,400,450)
        self.setWindowTitle('Drawing')
        self.show()

    def paintEvent(self,event):
        qp=QPainter()
        qp.begin(self)

        # 文本
        self.drawTextStr(event,qp)
        # 点
        self.drawPointers(qp)
        # color 矩形
        self.drawRectangles(qp)
        # Qpen画笔，用来画直线曲线椭圆等形状(形状没有试)
        self.drawLines(qp)
        # QBrush 画刷
        self.drawBrushes(qp)
        # 贝塞尔曲线
        self.drawBezierCurve(qp)

        qp.end()

    def drawTextStr(self,event,qp):
        qp.setPen(QColor(68,24,3))
        qp.setFont(QFont('Microsoft Yahei',19))
        qp.drawText(event.rect(),Qt.AlignCenter,self.text)

    def drawPointers(self,qp):
        qp.setPen(Qt.red)
        size=self.size()
        for i in range(3000):
            # 只绘制点到左上角
            x=random.randint(1,size.width()//2) 
            y=random.randint(1,size.height()//2)
            qp.drawPoint(x,y)

    def drawRectangles(self,qp):
        col=QColor()
        col.setNamedColor('#00f')
        qp.setPen(col)

        qp.setBrush(QColor(200, 0, 0))
        qp.drawRect(10, 15, 90, 60)

        qp.setBrush(QColor(0, 200, 0, 150))
        qp.drawRect(130, 15, 90, 60)

        qp.setBrush(QColor(0, 0, 200, 100))
        qp.drawRect(250, 15, 90, 60)

    def drawLines(self,qp):
        pen = QPen(Qt.gray, 3, Qt.SolidLine)

        qp.setPen(pen)
        qp.drawLine(20, 300, 400, 0)

        pen.setStyle(Qt.DashLine)
        qp.setPen(pen)
        qp.drawLine(20, 320, 400, 0)

        pen.setStyle(Qt.DashDotLine)
        qp.setPen(pen)
        qp.drawLine(20, 340, 400, 0)

        pen.setStyle(Qt.DotLine)
        qp.setPen(pen)
        qp.drawLine(20, 360, 400, 40)

        pen.setStyle(Qt.DashDotDotLine)
        qp.setPen(pen)
        qp.drawLine(20, 380, 400, 40)

        pen.setStyle(Qt.CustomDashLine)
        pen.setDashPattern([1, 4, 5, 4])
        qp.setPen(pen)
        qp.drawLine(20, 400, 400, 40)

    def drawBrushes(self,qp):
        # 上面的Pen会影响这里的边框
        brush = QBrush(Qt.Dense1Pattern)
        qp.setBrush(brush)
        qp.drawRect(20,200,40,90)

        qp.setPen(QPen(Qt.red, 2, Qt.SolidLine)) # 重新设置Pen
        brush.setStyle(Qt.Dense6Pattern)
        qp.setBrush(brush)
        qp.drawRect(70,200,40,90)

    def drawBezierCurve(self,qp):
        path=QPainterPath()
        path.moveTo(120,200)
        path.cubicTo(120,200,200,350,350,120)
        path.cubicTo(350,120,200,400,300,400)
        path.cubicTo(300,400,200,400,120,200)
        qp.drawPath(path)

if __name__ == '__main__':
    app=QApplication(sys.argv)
    ex=Example()
    sys.exit(app.exec_())