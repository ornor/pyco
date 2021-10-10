import re
import time
import abc
import functools
import collections

class Singleton(type):
    """
    Metaclass om een normale klasse te tronsformeren naar een singleton.
    Ieder nieuwe instantie van klasse wordt genegeerd en er wordt altijd
    de eerste instantie (object) gebruikt.

    class MyClass(BaseClass, metaclass = Singleton):
        pass
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ObjectTeller(metaclass = Singleton):
    """
    ObjectTeller zorgt ervoor dat over hele applicatie objecten een nieuw
    oplopend nummer krijgen. Hierdoor kan achteraf gekeken worden welk object
    eerder was aangemaakt.

    import pyco.basis as pycob

    teller = pycob.ObjectTeller()
    self.object_nummer = teller.object_nummer
    """

    _object_teller = 0

    def __init__(self):
        pass

    @property
    def object_nummer(self):
        self._object_teller += 1
        return self._object_teller




#==============================================================================
# ontwikkelaars tools:

def trace(func):
    """
    Decorator function useful for debugging.
    """
    @functools.wraps(func)
    def call(*args, **kwargs):
        sep = ', '
        msg = '>>> tracing {}: '.format(func.__name__)
        max_char = 30
        max_char_fill = ' ... '
        return_fill = '  -->  '

        def parse_arg(arg):
            str_arg = str(arg)
            if len(str_arg) > 2 and str_arg[0] == '<' and str_arg[-1] == '>':
                str_arg = re.split(r'\s', str_arg)[0] + '>'
            str_arg = str_arg if len(str_arg) < (2 * max_char - 2) else str_arg[:max_char] + max_char_fill + str_arg[-max_char:]
            return str_arg

        for arg in args:
            msg += parse_arg(arg) + sep

        for key, value in kwargs.items():
            msg += str(key) + ' = ' + parse_arg(value) + sep

        if msg.endswith(sep):
            msg = msg[:-len(sep)]

        start_time = int(round(time.time() * 1000))
        result = func(*args, **kwargs)
        end_time = int(round(time.time() * 1000))
        msg += return_fill + parse_arg(result)

        msg += '  [{} ms]'.format(end_time - start_time)

        msg = re.sub(r'\n', r'\\n', msg)
        print(msg)
        return result

    return call


def timer(name: str = '', disabled: bool = False):
    """
    Timer tool.
    t = timer('Name timer')
    t('first measure point')
    t('second measure point')
    """

    init_time = int(round(time.time() * 1000))
    prefix = '==>  '

    if name == '':
        msg = 'timer: start'
    else:
        msg = 'timer {}: 0 ms  (start)'.format(name)
    if not disabled:
        print(prefix + msg)

    def call(label: str = ''):
        cur_time = int(round(time.time() * 1000))
        if name == '':
            if label == '':
                msg = 'timer: {} ms'.format(cur_time - init_time)
            else:
                msg = 'timer: {} ms  ({})'.format(cur_time - init_time, label)
        else:
            if label == '':
                msg = 'timer {}: {} ms'.format(name, cur_time - init_time)
            else:
                msg = 'timer {}: {} ms  ({})'.format(name, cur_time - init_time, label)
        if not disabled:
            print(prefix + msg)

    return call


class BaseDescriptor:
    __counter = 0

    def __init__(self):
        cls = self.__class__
        prefix = cls.__name__
        index = cls.__counter
        self.storage_name = '_{}#{}'.format(prefix, index)
        cls.__counter += 1

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return getattr(instance, self.storage_name)

    def __set__(self, instance, value):
        setattr(instance, self.storage_name, value)


class ValidatedDescriptor(abc.ABC, BaseDescriptor):
    """
    class Quantity(ValidatedDescriptor):
        def validate(self, instance, value):
            if value <= 0:
                raise ValueError('Value must be greater than 0.')

    class NonBlank(ValidatedDescriptor):
        def validate(self, instance, value):
            value = value.strip()
            if len(value) == 0:
                raise ValueError('Value cannot be empty or blank.')
            return value

    class LineItem:
        description = NonBlank()
        weight = Quantity()
        price = Quantity()

        def __init__(self, description, weight, price):
            self.description = description
            self.weight = weight
            self.price = price

        def subtotal(self):
            return self.weight * self.price

    """

    def __set__(self, instance, value):
        value = self.validate(instance, value)
        super().__set__(instance, value)

    @abc.abstractmethod
    def validate(self, instance, value):
        """ Return validated value or raise ValueError """


class FrozenAttr():
    """
    An immutable mapping object.

    Use keyword/values to construct. Or use 'from_dict' class method to
    construct from dict.
    Values can be retreived by getting attribute (keyword).

    >>> fd = FrozenAttr(a = 43, b = 4, c = True)
    >>> value_a = fd.a
    """

    def __new__(self, **args):
        data_dict = dict(**args)
        FrozenAttr = collections.namedtuple('FrozenAttr', data_dict.keys())
        return FrozenAttr(*data_dict.values())

    @classmethod
    def from_dict(cls, mutable_dict: dict):
        return cls(**mutable_dict)


class cached_property(property):
    """A decorator that converts a function into a lazy property. The
    function wrapped is called the first time to retreive the result,
    and then that calculated result is used te next time you access
    the value::

        class Foo(object):
            @cached_property
            def foo(self):
                #calculate someting important here
                return 42

    The class has te have a `__dict__` in order for this property to
    work.
    """

    def __init__(self, func, name=None, doc=None):
        self.__name__ = name or func.__name__
        self.__module__ = func.__module__
        self.__doc__ = doc or func.__doc__
        self.func = func

    def __set__(self, obj, value):
        obj.__dict__[self.__name__] = value

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        _missing = []  # some dummy object
        value = obj.__dict__.get(self.__name__, _missing)
        if value is _missing:
            value = self.func(obj)
            obj.__dict__[self.__name__] = value
        return value
