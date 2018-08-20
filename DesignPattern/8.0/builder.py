# 建造者模式

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


class order(object):
    '''订单类'''
    def __init__(self, orderBuilder):
        '''这里的 orderBuilder 为建造者'''
        self.burger = orderBuilder.burger
        self.snack = orderBuilder.snack
        self.beverage = orderBuilder.beverage

    def show(self):
        print("burger:",self.burger.getName())
        print("snack:", self.snack.getName())
        print("beverage:", self.beverage.getName())


class orderBuilder(object):
    def addBurger(self, burger):
        self.burger = burger
    def addSnack(self, snack):
        self.snack = snack
    def addBeverage(self, beverage):
        self.beverage = beverage
    def build(self):
        return order(self)

if __name__ == '__main__':
    orderBuilder = orderBuilder()
    orderBuilder.addBurger(spicyChickenBurger())
    orderBuilder.addSnack(chickenWings())
    orderBuilder.addBeverage(coke())

    orderBuilder.build().show()

