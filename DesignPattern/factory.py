#工厂模式

# 主食
class Burger():
    def __init__(self, name='', price=0.0):
        self.name=name
        self.price=price
        self.type='BURGER'
    def getPrice(self):
        return self.price
    def setPrice(self,price):
        self.price=price
    def getName(self):
        return self.name

class cheeseBurger(Burger):
    def __init__(self):
        super().__init__("cheese burger", 10.0)

class spicyChickenBurger(Burger):
    def __init__(self):
        super().__init__("spicy chicken burger", 15.0)

# 小吃
class Snack():
    def __init__(self, name='', price=0.0):
        self.name=name
        self.price=price
        self.type='SNACK'
    def getPrice(self):
        return self.price
    def setPrice(self, price):
        self.price = price
    def getName(self):
        return self.name

class chips(Snack):
    def __init__(self):
        super().__init__("chips", 6.0)

class chickenWings(Snack):
    def __init__(self):
        super().__init__("chicken wings", 12.0)

# 饮料
class Beverage():
    def __init__(self, name='', price=0.0):
        self.name=name
        self.price=price
        self.type='BEVERAGE'
    def getPrice(self):
        return self.price
    def setPrice(self, price):
        self.price = price
    def getName(self):
        return self.name

class coke(Beverage):
    def __init__(self):
        super().__init__("coke", 4.0)

class milk(Beverage):
    def __init__(self):
        super().__init__("milk", 5.0)

# 工厂
class SimpleFoodFactory():
    '''简单工厂模式'''
    @classmethod
    def createFood(self,foodClass):
        print(" factory produce a instance.")
        foodIns=foodClass()
        return foodIns

if  __name__=="__main__":
    cheese_burger=SimpleFoodFactory.createFood(cheeseBurger)
    print(cheese_burger.__dict__)
    chicken_wings=SimpleFoodFactory.createFood(chickenWings)
    print(chicken_wings.__dict__)
    coke_drink=SimpleFoodFactory().createFood(coke)
    print(coke_drink.__dict__)