from Config import *
import copy
class Point:
    '''每个点，包含坐标和颜色'''
    def __init__(self, x, y, rgb=(255,255,255)):
        self.x = x
        self.y = y
        self.rgb = rgb

class AllPoint(object):
    '''存储所有的点'''
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.area=[[0 for i in range(ConWidth)] for i in range(ConHeight)]
        print(len(self.area))
        return 
        p1=Point(0,0)
        for i in range(self.width):
            for j in range(self.height):

                self.area.append( Point(i, j, (int(i*(256/self.width)), int(j*(256/self.height)), int(j*(256/self.height))) ) )
                #p2.x,p2.y,p2.rgb=i,j, (int(i*(256/self.width)), int(j*(256/self.height)), int(j*(256/self.height)))
                #qp.setPen(QColor(int(i*(256/self.width)), int(j*(256/self.height)), int(j*(256/self.height))))
                #qp.drawPoint(i,j)
import time
start = time.perf_counter()
# print('start')
board=AllPoint(ConWidth, ConHeight)
# print(board.area)
end = time.perf_counter()
print("--- ok ---> spend time: ",end-start)  #debug 1.3-1.5s  nodebug 0.2s 
