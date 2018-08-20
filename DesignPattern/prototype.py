#原型模式
import copy
 
class Point:
    def __init__(self, x, y, l):
        print(l)
        self.x = x
        self.y = y
        self.l = l

p1=Point(1,2,[1,2,3])
p2=copy.copy(p1) # 浅拷贝
p3=copy.deepcopy(p1) # 深拷贝

p1.x=0 # 修改 不可改变对象
p1.l.append(4) # 修改（列表）可改变对象 （浅拷贝只会复制原列表的引用，指向同一个对象，所以修改时会更改p2.l）

print(p1, p1.__dict__)
print(p2, p2.__dict__)
print(p3, p3.__dict__)