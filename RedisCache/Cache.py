# coding:utf-8
""" 缓存类 """

from Instance import _instance_redis
import json
import sys
import os
import hashlib
import logging
import functools
logging.basicConfig(level=logging.DEBUG)


class Cache(object):

    def __init__(self, key=None):
        # 指定key
        self._key = key
        # 缓存函数
        self._cache_func = None
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

        if self._key:
            """ 使用指定Key """
            key = self._key
            logging.debug("key: %s" % key)
            return key

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

        # 过滤参数中的self对象
        args_temp = self._cache_func.args
        # 拿到类函数对象的类名和类对象的类名
        func_class_name = os.path.splitext(self._cache_func.__qualname__)[0]
        obj_class_name = self._cache_func.args[0].__class__.__name__
        if isinstance(args_temp[0], object) and func_class_name == obj_class_name:
            args_temp = args_temp[1:]

        ret_list.append(
            def_sha1(
                str(args_temp) + str(self._cache_func.kwargs)
            )
        )
        logging.debug('key:'+':'.join(ret_list))
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

    def __call__(self, func):
        """ 调用缓存 """
        self._cache_func = func

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 存储函数参数

            self._cache_func.args = args
            self._cache_func.kwargs = kwargs

            # 获取key，获取缓存
            key = self.key()
            cache = self.get(key)

            # 删除缓存
            if self._delete:
                self._delete = True
                return self.delete(key)

            # 更新缓存
            if not cache or self._update:
                self._update = False
                data = func(*args, **kwargs)
                value = json.dumps(data)

                if self.set(key, value):
                    return data
                return False

            return json.loads(cache)
        return wrapper


if __name__ == '__main__':
    c = Cache()
    c.key()
