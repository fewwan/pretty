#autor: fewwan
#from:https://stackoverflow.com/a/26209900/12757078
from typing import *
from math import inf

__all__ = ['pretty', 'Formatter', 'pprint']

class Formatter(object):
    def __init__(self) -> NoReturn:
        self.types:dict = {}
        self.inch:str = ' ' # indent character
        self.nlch:str = '\n' # new line character
        self.indent:int = 4 # indent
        self.deep:int = inf # deep
        # # TODO: implement
        self.compact:boolean = False # align to key
        self._indent:int = self.indent
        self.set_formater(object, self.__class__.format_object)
        self.set_formater(dict, self.__class__.format_dict)
        self.set_formater(list, self.__class__.format_list)
        self.set_formater(tuple, self.__class__.format_tuple)

    def __call__(self, *args:Tuple[object, ...], indent=None, deep=None, compact=None, **kargs:dict) -> str:
        if indent: self.indent = indent
        if deep:self.deep = deep
        if compact: self.compact = compact
        self._indent = self.indent
        result=[]
        if args:
            if len(args)>1:
                result.append(self.nlch.join([self.format(value, self.indent) for value in args]))
            else:
                result.append(self.format(args[0], self.indent))
        if kargs:
            result.append(self.nlch.join(['%s = %s' % (key, self.format(value, self.indent)) for key, value in kargs.items()]))

        return self.nlch.join(result)

    def set_formater(self, obj:type, callback:Callable[[object, object, int], str]) -> NoReturn:
        self.types[obj] = callback

    def get_formater(self, obj:type) -> Callable:
        return self.types[type(obj) if type(obj) in self.types else object]

    def format(self, value:object, indent:int) -> str:
        return self.get_formater(value)(self, value, indent)



    def format_object(self, value:object, indent:int) -> str:
        return repr(value)

    def format_dict(self, value:dict, indent:int) -> str:
        items = [
            self.nlch + self.inch * indent + repr(k) + ': ' +
            self.format(v, indent + self._indent) if indent//self._indent <= self.deep else repr(v)
            for k,v in value.items()
        ]
        return '{%s}' % (','.join(items) + self.nlch + self.inch * (indent - self._indent) if indent//self._indent <= self.deep else ', '.join(items))

    def format_list(self, value:list, indent:int) -> str:
        items = [
            self.nlch + self.inch * indent + self.format(item, indent + self._indent) if indent//self._indent <= self.deep else repr(item)
            for item in value
        ]
        return '[%s]' % (','.join(items) + self.nlch + self.inch * (indent - self._indent) if indent//self._indent <= self.deep else ', '.join(items))

    def format_tuple(self, value:tuple, indent:int) -> str:
        items = [
            self.nlch + self.inch * indent + self.format(item, indent + self._indent) if indent//self._indent <= self.deep else repr(item)
            for item in value
        ]
        return '(%s)' % (','.join(items) + self.nlch + self.inch * (indent - self._indent) if indent//self._indent <= self.deep else ', '.join(items))


pretty = Formatter()

from collections import deque, ChainMap, Counter, OrderedDict


def format_deque(self, value:deque, indent:int) -> str:
    items = [
        self.nlch + self.inch * indent + self.format(item, indent + self._indent) if indent//self._indent <= self.deep else repr(item)
        for item in value
    ]
    return 'deque(%s)' % (','.join(items) + self.nlch + self.inch * (indent - self._indent) if indent//self._indent <= self.deep else ', '.join(items))

pretty.set_formater(deque, format_deque)


def format_ChainMap(self, value:ChainMap, indent:int) -> str:
    items = [
        self.nlch + self.inch * indent + repr(k) + ': ' +
        self.format(v, indent + self._indent) if indent//self._indent <= self.deep else repr(v)
        for k,v in value.items()
    ]
    return 'ChainMap(%s)' % (','.join(items) + self.nlch + self.inch * (indent - self._indent) if indent//self._indent <= self.deep else ', '.join(items))

pretty.set_formater(ChainMap, format_ChainMap)


def format_Counter(self, value:Counter, indent:int) -> str:
    items = [
        self.nlch + self.inch * indent + repr(k) + ': ' + repr(v)
        for k,v in value.items()
    ]
    return 'Counter(%s)' % (','.join(items) + self.nlch + self.inch * (indent - self._indent) if indent//self._indent <= self.deep else ', '.join(items))

pretty.set_formater(Counter, format_Counter)


def format_OrderedDict(self, value:OrderedDict, indent:int) -> str:
    items = [
        self.nlch + self.inch * indent + repr(k) + ': ' +
        self.format(v, indent + self._indent) if indent//self._indent <= self.deep else repr(v)
        for k,v in value.items()
    ]
    return 'OrderedDict(%s)' % (','.join(items) + self.nlch + self.inch * (indent - self._indent) if indent//self._indent <= self.deep else ', '.join(items))

pretty.set_formater(OrderedDict, format_OrderedDict)

from nbt.nbt import _TAG_End, TAG_Byte, TAG_Short, TAG_Int, TAG_Long, TAG_Float, TAG_Double, TAG_Byte_Array, TAG_String, TAG_List, TAG_Compound, TAG_Int_Array, TAG_Long_Array

def format__TAG_End(self, value:_TAG_End, indent:int) -> str:
    return value.pretty_tree()

pretty.set_formater(_TAG_End, format__TAG_End)



def format_TAG_Byte(self, value:TAG_Byte, indent:int) -> str:
    return value.pretty_tree()

pretty.set_formater(TAG_Byte, format_TAG_Byte)



def format_TAG_Short(self, value:TAG_Short, indent:int) -> str:
    return value.pretty_tree()

pretty.set_formater(TAG_Short, format_TAG_Short)



def format_TAG_Int(self, value:TAG_Int, indent:int) -> str:
    return value.pretty_tree()

pretty.set_formater(TAG_Int, format_TAG_Int)



def format_TAG_Long(self, value:TAG_Long, indent:int) -> str:
    return value.pretty_tree()

pretty.set_formater(TAG_Long, format_TAG_Long)



def format_TAG_Float(self, value:TAG_Float, indent:int) -> str:
    return value.pretty_tree()

pretty.set_formater(TAG_Float, format_TAG_Float)



def format_TAG_Double(self, value:TAG_Double, indent:int) -> str:
    return value.pretty_tree()

pretty.set_formater(TAG_Double, format_TAG_Double)



def format_TAG_Byte_Array(self, value:TAG_Byte_Array, indent:int) -> str:
    return value.pretty_tree()

pretty.set_formater(TAG_Byte_Array, format_TAG_Byte_Array)



def format_TAG_String(self, value:TAG_String, indent:int) -> str:
    return value.pretty_tree()

pretty.set_formater(TAG_String, format_TAG_String)



def format_TAG_List(self, value:TAG_List, indent:int) -> str:
    return value.pretty_tree()

pretty.set_formater(TAG_List, format_TAG_List)



def format_TAG_Compound(self, value:TAG_Compound, indent:int) -> str:
    return value.pretty_tree()

pretty.set_formater(TAG_Compound, format_TAG_Compound)



def format_TAG_Int_Array(self, value:TAG_Int_Array, indent:int) -> str:
    return value.pretty_tree()

pretty.set_formater(TAG_Int_Array, format_TAG_Int_Array)



def format_TAG_Long_Array(self, value:TAG_Long_Array, indent:int) -> str:
    return value.pretty_tree()

pretty.set_formater(TAG_Long_Array, format_TAG_Long_Array)

# from itertools import count, cycle, repeat, accumulate, chain, compress, dropwhile, filterfalse, islice, starmap, takewhile, zip_longest


def pprint(*args, **kwargs): print(pretty(*args, **kwargs))


if __name__=='__main__':
    testdict = {'list':['a','b',1,2,['a','b',1,2]],'dict':{'a':1,2:'b','dict':{'a':1,2:'b'}},'tuple':('a','b',1,2,('a','b',1,2)),'function':pretty,'unicode':u'\xa7',('tuple','key'):'valid'}
    pprint(testdict)
