# -*- coding: utf-8 -*-

"""Use singleton design pattern for config.

Using class attributes has several disadvantages. For exmaple, it cannot
override the setter function for more flexible attribute assignment. It also
does not support __str__ function to print the config. The downside is that
sphinx cannot show the default values of instance attributes.

"""

class Singleton(type):
    """Singleton design pattern. This should be used as metaclass.

    Note:
        This version does not support passing args during first time
        construction.

    """
    _instance = None
    def __call__(cls):
        setattr = cls.__setattr__
        cls.__setattr__ = object.__setattr__
        if cls._instance is None:
            cls._instance = super().__call__()
            cls.__setattr__ = setattr
        return cls._instance


class Config(metaclass=Singleton):

    def __init__(self):
        self._config = list()

    def __setattr__(self, name, value):
        if name not in self._config:
            message = '%s is unknown. Use "add_attr" to add new attribute.'
            message = message % (name)
            raise RuntimeError(message)
        else:
            super().__setattr__(name, value)

    def add_config(self, name, default_value):
        self._config.append(name)
        setattr(self, name, default_value)

    def __str__(self):
        """Prints out all configurations."""
        max_config_len = max([len(c) for c in self._config])
        message = list()
        name = '.'.join([self.__class__.__module__, self.__class__.__name__])
        message.append(name + ':')
        pattern = '    %%%ds: %%s' % max_config_len
        for key in self._config:
            value = str(getattr(self, key))
            message.append(pattern % (key, value))
        max_line_len = max([len(l) for l in message])
        message.insert(0, '-' * max_line_len)
        message.append('-' * max_line_len)
        return '\n'.join(message)
