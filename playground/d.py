# coding:utf-8
'''来自http://eli.thegreenplace.net/2011/08/14/python-metaclasses-by-example'''

class MetaClass(type):

    def __new__(meta, name, bases, dct):
        print('-----------------------------------')
        print("Allocating memory for class", name)
        print(meta)
        print(bases)
        print(dct)
        return super(MetaClass, meta).__new__(meta, name, bases, dct)

    def __init__(cls, name, bases, dct):
        print('-----------------------------------')
        print("Initializing class", name)
        print(cls)
        print(bases)
        print(dct)

        dct['__mappings__'] = {"u": "name"}
        super(MetaClass, cls).__init__(name, bases, dct)


class Myclass(object, metaclass=MetaClass):

    # __metaclass__ = MetaClass

    def __init__(self, **kwargs):
        super().__init__()

    def foo(self, param):
        print (param)

print("========================")
p = Myclass(my="my")
p.foo("hello")
# print(p.u)
# -----------------------------------
# Allocating memory for class Myclass
# <class '__main__.MetaClass'>
# (<type 'object'>,)
# {'__module__': '__main__', 'foo': <function foo at 0x1007f6500>, '__metaclass__': <class '__main__.MetaClass'>}
# -----------------------------------
# Initializing class Myclass
# <class '__main__.Myclass'>
# (<type 'object'>,)
# {'__module__': '__main__', 'foo': <function foo at 0x1007f6500>, '__metaclass__': <class '__main__.MetaClass'>}
# hello