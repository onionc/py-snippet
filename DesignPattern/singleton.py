import time

class Singleton(object):
    '''抽象单例'''
    def __new__(self, *args, **kw):
        if not hasattr(self,'_instance'):
            self._instance = super().__new__(self, *args, **kw)
        return self._instance

class Boss(Singleton):
    '''BOSS类'''
    def __new__(self):
        self.hp=100
        self._maxHp=100
        return super().__new__(self)

    def decHp(self,hurt=0):
        '''攻击或者治疗'''
        if hurt>0:
            self.hp-=hurt
            self.hp = self.hp if self.hp>0 else 0
        elif hurt<0:
            self.hp-=hurt
            self.hp = self.hp if self.hp<self._maxHp else self._maxHp

        return self.hp

    def getHp(self):
        return self.hp

class Fighter(object):
    '''人物类'''
    def __init__(self, name, hp=100, attackVal=10):
        self.name=name
        #self.hp=hp
        #self.attackVal=attackVal

    def attack(self, value=0):
        b=Boss()
        b.decHp(value)
        print("{0}| {1} -> boss, {2} {3} . [Boss hp={4}]".format(time.strftime("%M:%S",time.localtime()), self.name,'伤害' if value>=0 else '治疗',abs(value),b.getHp()))
        

if __name__ == '__main__':
    
    mt=Fighter("哀木涕")
    mt.attack(10)
    lr=Fighter("劣人")
    lr.attack(-3)
    dz=Fighter("呆呆贼")
    dz.attack(12)