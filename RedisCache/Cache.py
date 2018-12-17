# coding:utf-8
""" 缓存类 """

from Instance import _instance_redis
import json
import sys
import os
import hashlib
import logging
logging.basicConfig(level=logging.DEBUG)


class Cache(object):

    def __init__(self, func=None):
        # 获取缓存函数
        self._cache_func = func
        # redis实例
        self._redis = _instance_redis
        # 过期时间
        self._ttl = 7200
        # 更新标志
        self._update = False
        # 删除标志
        self._delete = False

    def key(self):
        """ 生成Key """

        # trace_hash_list = []  # 待哈希列表
        trace_list = []  # 待字符串列表

        f = sys._getframe(2)
        # f = f.f_back    # 第一次是key函数自身，忽略
        # f = f.f_back    # 第二次是Cache文件的__call__，忽略

        while hasattr(f, "f_code"):
            """ 拿到调用堆栈，除函数 """
            co = f.f_code
            filename = os.path.basename(co.co_filename)
            coname = co.co_name
            if not filename:
                continue
            # 函数名，如果存在，不存在则为<module>
            trace_list.insert(0, os.path.splitext(coname)[0])
            # 文件名
            trace_list.insert(0, os.path.splitext(filename)[0])

            '''
            temp = "{0}({1}:{2})".format(
                filename,
                coname,
                f.f_lineno
            )
            trace_hash_list.insert(0, temp)
            '''
            f = f.f_back

        # 哈希函数 PEP-8不建议用lambda
        def_sha1 = lambda s: hashlib.md5(
            str(s).encode('utf-8')
        ).hexdigest().upper()
        # 有效堆栈字符串:堆栈哈希值:缓存函数:参数哈希值
        ret_list = []
        ret_list.append(':'.join(trace_list))
        # ret_list.append(def_sha1(trace_hash_list))
        ret_list.append(self._cache_func.__name__)
        ret_list.append(
            def_sha1(
                str(self._cache_func.args) + str(self._cache_func.kwargs)
            )
        )
        print('key:'+':'.join(ret_list))
        return ':'.join(ret_list)

    def set(self, key=None, value=None):
        """ 设置缓存 """
        if not key:
            key = str(self.key())
        return self._redis.set(key, value, self._ttl)

    def get(self, key):
        """ 获取缓存 """
        return self._redis.get(key)

    def delete(self, key):
        """ 删除缓存 """
        return self._redis.delete(key)

    def remove(self, pattern):
        """ 批量删除缓存 """
        del_count = 0
        keys = self._redis.keys(pattern)
        for key in keys:
            if self.delete(key):
                del_count += 1
        return del_count

    def set_attr(self, **attr):
        """ 设置属性 """
        allows = ['update', 'delete', 'ttl']
        for k in attr:
            if k in allows:
                name = str("_"+k)
                setattr(self, name, attr[k])
        return self

    def __call__(self, *args, **kwargs):
        """ 调用缓存方法 """

        # 存储函数参数
        self._cache_func.args = args
        self._cache_func.kwargs = kwargs

        # 获取key，取缓存
        key = self.key()
        cache = self.get(key)

        # 删除缓存
        if self._delete:
            self._delete = True
            return self.delete(key)

        # 更新缓存
        if not cache or self._update:
            self._update = False
            data = self._cache_func(*args, **kwargs)
            value = json.dumps(data)

            if self.set(key, value):
                return data
            return False

        return json.loads(cache)


if __name__ == '__main__':
    c = Cache()
    c.key()
