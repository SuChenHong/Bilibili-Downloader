# -*- coding: utf-8 -*-
from inspect import getfullargspec


class Function:

    def __init__(self, fn):
        self.fn = fn

    def __call__(self, *args, **kwargs):

        fn = Namespace.get_instance().get(self.fn, *args)
        if not fn:
            raise Exception('没有匹配的函数')

        return fn(*args, **kwargs)

    def key(self, args=None):

        if args is None:
            args = getfullargspec(self.fn).args

        return tuple([
            self.fn.__module__,
            self.fn.__class__,
            self.fn.__name__,
            len(args or []),
        ])


class Namespace(object):

    __instance = None

    def __init__(self):

        if self.__instance is None:
            self.function_map = dict()
            Namespace.__instance = self
        else:
            raise Exception('不能再实例化一个虚拟命名空间')

    @staticmethod
    def get_instance():

        if Namespace.__instance is None:
            Namespace()
        return Namespace.__instance

    def register(self, fn):

        func = Function(fn)
        self.function_map[func.key()] = fn
        return func

    def get(self, fn, *args):

        func = Function(fn)
        return self.function_map.get(func.key(args=args))


def overload(fn):
    """ 实现函数重载 """
    return Namespace.get_instance().register(fn)


# @overload
# def area(l, b):
#     return l*b
#
#
# @overload
# def area(r):
#     import math
#     return math.pi * r ** 2
#
#
# print(area(3, 4))
# print(area(7))

