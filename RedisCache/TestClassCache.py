# coding:utf-8
""" 类函数缓存测试 """
from Cache import Cache


class Manager():
    """ 测试类函数缓存 """
    @Cache()
    def search_manager(self, district=1):
        print("into search manager func.")
        return list(range(district))


@Cache()
def search_manager(obj, district=1):
    """ 测试对象过滤 """
    print("into search manager func.")
    return list(range(district))


if __name__ == '__main__':
    a1 = Manager().search_manager()
    print(a1)
    a2 = Manager().search_manager(2)
    print(a2)
    a3 = Manager().search_manager(2)
    print(a3)
    print("test object: ---------------")
    m1 = Manager()
    m2 = Manager()
    b1 = search_manager(m1, 2)
    b2 = search_manager(m1, 2)
    b3 = search_manager(m2, 2)
