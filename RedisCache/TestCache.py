# coding:utf-8
""" 单函数缓存测试 """
from Cache import Cache


@Cache
def all_data(status):
    """ 缓存数据 """
    print(f"this is all data, args={status}")
    return list(range(status))


class TestC(object):
    def get(self):
        t1 = all_data(10)
        return t1


if __name__ == '__main__':
    a1 = all_data(10)
    print(a1)
    a2 = all_data(10)
    print(a2)
    a3 = all_data(1)
    print(a3)
    a4 = TestC().get()
    print(a4)
