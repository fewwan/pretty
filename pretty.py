#autor: fewwan
#from:https://stackoverflow.com/a/26209900/12757078
from typing import *
from math import inf

__all__ = ['pretty', 'Formatter', 'pprint', 'info']

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
        self.set_formater(set, self.__class__.format_set)
        self.set_formater(frozenset, self.__class__.format_frozenset)

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

    def format_set(self, value:set, indent:int) -> str:
        items = [
            self.nlch + self.inch * indent + self.format(item, indent + self._indent) if indent//self._indent <= self.deep else repr(item)
            for item in value
        ]
        return '{%s}' % (','.join(items) + self.nlch + self.inch * (indent - self._indent) if indent//self._indent <= self.deep else ', '.join(items))
    
    def format_frozenset(self, value:frozenset, indent:int) -> str:
        items = [
            self.nlch + self.inch * indent + self.format(item, indent + self._indent) if indent//self._indent <= self.deep else repr(item)
            for item in value
        ]
        return 'frozenset({%s})' % (','.join(items) + self.nlch + self.inch * (indent - self._indent) if indent//self._indent <= self.deep else ', '.join(items))
    
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

# from itertools import count, cycle, repeat, accumulate, chain, compress, dropwhile, filterfalse, islice, starmap, takewhile, zip_longest


def pprint(*args, **kwargs): print(pretty(*args, **kwargs))
def info(obj, magic_methods=True): return {_:getattr(obj, _) for _ in dir(obj) if (not _.startswith('__') if not magic_methods else True)}

if __name__=='__main__':
    testdict = {'list':['a','b',1,2,['a','b',1,2]],'dict':{'a':1,2:'b','dict':{'a':1,2:'b'}},'tuple':('a','b',1,2,('a','b',1,2)),'function':pretty,'unicode':u'\xa7',('tuple','key'):'valid'}
    pprint(testdict)
