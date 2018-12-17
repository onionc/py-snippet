# coding:utf-8
""" 单函数缓存测试 """
from Cache import Cache


@Cache()
def all_data(status):
    """ 缓存数据 """
    print(f"this is all data, args={status}")
    return list(range(status))


class TestC(object):
    """ 类中调用查看堆栈不同 """
    def get(self):
        t1 = all_data(10)
        return t1


@Cache(key='X0011')
def all_data_key(status):
    """ 指定Key的缓存数据 """
    print(f"this is all data (use key), args={status}")
    return list(range(status))


if __name__ == '__main__':
    a1 = all_data(10)
    print(a1)
    a2 = all_data(10)
    print(a2)
    a3 = all_data(1)
    print(a3)
    a4 = TestC().get()
    print(a4)
    print("use key: -------------------------- ")
    a5 = all_data_key(4)
    print(a5)
    a6 = all_data_key(5)
    print(a6)
