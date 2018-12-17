# coding:utf-8
""" 测试 缓存设置属性 """
from Cache import Cache


@Cache()
def attack_start(mul=1):
    print("战斗开始......")
    return 'attack ' * mul


if __name__ == "__main__":
    attack_start.set_attr(update=True, ttl=200)
    a1 = attack_start(3)
    print(a1)
    attack_start.set_attr(update=True, ttl=100)
    a2 = attack_start(3)
    print(a2)
    attack_start.set_attr(delete=True)
    a3 = attack_start(3)
    print(a3)