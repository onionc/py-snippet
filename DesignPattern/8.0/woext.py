import time
import random
from Log import warLog

class Singleton(object):
    '''抽象单例'''
    def __new__(self, *args, **kw):
        if not hasattr(self,'_instance'):
            self._instance = super().__new__(self, *args, **kw)
        return self._instance

class Boss(Singleton):
    '''BOSS类'''
    def __new__(self, *args, **kw):
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
    '''抽象人物类'''
    def __init__(self, name, hp=100, attackVal=10):
        self.name=name
        self.hp=hp
        self.attackVal=attackVal

    def attack(self):
        value=self.attackVal
        
        b=Boss()
        b.decHp(value)
        message="{0} -> boss, {1} {2} . [Boss hp={3}]".format( self.name,'伤害' if value>=0 else '治疗',abs(value),b.getHp())
        warLog.show(message)

class Warrior(Fighter):
    '''战士'''
    name='战士'
    def __init__(self, name=""):
        if name: self.name=str(name)
        super().__init__(self.name, 150, 10)

class Hunter(Fighter):
    '''猎人'''
    name='猎人'
    def __init__(self, name=""):
        if name: self.name=str(name)
        super().__init__(self.name, 100, 8)

class Rogue(Fighter):
    '''盗贼'''
    name='盗贼'
    def __init__(self, name=""):
        if name: self.name=str(name)
        super().__init__(self.name, 80, 12)

class Shaman(Fighter):
    '''萨满'''
    name='萨满'
    def __init__(self, name=""):
        if name: self.name=str(name)
        super().__init__(self.name, 80, 6)

class WarFactory(object):
    '''战争工厂'''
    @classmethod
    def createFighter(self, fighter, name=''):
        return fighter(name)

# 建造模式，用来组队

class TeamUp(object):
    '''组队（生产）'''
    def __init__(self, teamName="小队"):
        self.teamName=teamName
        self.total=4
        self.zs=None
        self.ls=None
        self.dz=None
        self.sm=None
        self.team=[]
        warLog.show("来人啊，我们{0}要组队了".format(self.teamName))

    def enrollment(self, fighter):
        '''入队'''
        self.team.append(WarFactory.createFighter(fighter))
        warLog.show("{0} 入队一人：{1}".format(self.teamName,fighter.name))
    
    def __repr__(self):
        if len(self.team)==self.total:
            return "{0}成员：{1}, {2}, {3} 以及 {4}。".format(self.teamName,*[a.name for a in self.team])
        return "小组不足{0}人".format(self.total)

class TeamDirector(object):
    '''组队过程（步骤）'''
    def __init__(self, builder):
        self.group = builder
 
    def createTeam(self, zs, lr, dz, sm):
        '''入队人员'''
        self.group.enrollment(zs)
        self.group.enrollment(lr)
        self.group.enrollment(dz)
        self.group.enrollment(sm)
 
    def show(self):
        warLog.show(self.group)
 
if __name__ == '__main__':
    
    # 工厂模式
    # zs=WarFactory.createFighter(Warrior, '哀木涕')
    # zs.attack()
    # lr=WarFactory.createFighter(Hunter, '劣人')
    # lr.attack()
    # dz=WarFactory.createFighter(Rogue, '呆呆贼')
    # dz.attack()
    
    # 工厂模式 人海战术
    # while Boss().getHp()>0:
    #     r=random.choice([Warrior, Hunter, Rogue])
    #     WarFactory.createFighter(r).attack()

    # 建造者模式 菊爆小队
    team=TeamDirector(TeamUp('【菊爆小队】'))
    team.createTeam(Warrior, Hunter, Rogue, Shaman)
    team.show()

