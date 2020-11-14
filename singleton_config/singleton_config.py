# -*- coding: utf-8 -*-

"""Global configurations using singleton design pattern.

Using class attributes has several disadvantages. For exmaple, it cannot
override the setter function for more flexible attribute assignment. It also
does not support ``__str__`` function to print the config. The downside is that
sphinx cannot show the default values of instance attributes.

"""
import json


class Singleton(type):
    """Singleton design pattern. This should be used as metaclass.

    Note:
        This version does not support passing args during first time
        construction.

    """
    _instance = None
    def __call__(cls):
        if cls._instance is None:
            setattr = cls.__setattr__
            cls.__setattr__ = object.__setattr__
            cls._instance = super().__call__()
            cls.__setattr__ = setattr
        return cls._instance


class Config(metaclass=Singleton):
    """Configurations with singleton design pattern.

    By using singleton, each time users call ``Config()``, it will returns the
    same instance to ensure the configurations are consistent throughout a whole
    program.

    Note:
        Newly assigned config (as an attribute) should be registered via the
        method :meth:`add_config`. Simple ``=`` assigment will be denied if it
        is not registered.

    Users can inherit from this class to add more configurations during
    initialization.

    Note:
        Call ``super().__init__()`` in first line of the subclass ``__init__``.

    This class supports loading and saving. If the value conversion is desired
    during loading and saving, for example, an object need be converted into
    string to be written in a json file, implement methods ``_save_{name}`` and
    ``_load_{name}`` where ``{name}`` is the attribute name.

    To show the configurations, call

    >>> print(Config())

    """
    def __init__(self):
        self._config = list()
        self._private = list()

    def __setattr__(self, name, value):
        """Sets attr only when it has been added by :meth:`add_config`."""
        if (name not in self._config) and (name not in self._private):
            message = '%s is unknown. Use "add_config" to add new attribute.'
            message = message % (name)
            raise RuntimeError(message)
        else:
            super().__setattr__(name, value)

    def add_config(self, name, default_value, property=False):
        """Tracks a config.

        Args:
            name (str): The name of the attribute.
            default_value: The default value for this attribute.
            property (bool): Set '_' + name instead for property decoration to
                work appropriately.

        """
        self._config.append(name)
        if property:
            self._private.append('_' + name)
            setattr(self, '_' + name, default_value)
            self._define_default_property(name)
        else:
            setattr(self, name, default_value)

    def _define_default_property(self, name):
        if not hasattr(self, f'_set_{name}'):
            raise RuntimeError(f'_set_{name} is not defined.')
        exec(f'def {name}(self): return self._{name}')
        exec(f'self.__class__.{name} = property({name}, self.__class__._set_{name})')
        
    def __str__(self):
        """Prints out all configurations."""
        max_config_len = max([len(c) for c in self._config])
        message = list()
        name = '.'.join([self.__class__.__module__, self.__class__.__name__])
        message.append(name + ':')
        pattern = '    %%%ds: %%s' % max_config_len
        for key in sorted(self._config):
            value = str(getattr(self, key))
            message.append(pattern % (key, value))
        return '\n'.join(message)

    def has_config(self, name):
        """Tests if it contains this config.

        Args:
            name (str): The name of the config to test.

        Returns:
            bool: Whether it has this config.

        """
        return name in self._config

    def load_json(self, filepath):
        """Loads configurations from a ``".json"`` file.

        Args:
            filepath (str): The filepath to the json file.

        """
        with open(filepath) as jfile:
            loaded = json.load(jfile)
        self.load_dict(loaded)

    def load_dict(self, config):
        """Loads configurations from a :class:`dict`.

        Note:
            If a method ``_load_{config}`` exists, use that method to load this
            config.

        Args:
            config (dict): The configurations to load.

        """
        for key, value in config.items():
            load = '_load_%s' % key
            if hasattr(self, load):
                getattr(self, load)(value)
            else:
                setattr(self, key, value)

    def save_json(self, filepath):
        """Saves configurations into a ``".json"`` file.

        Args:
            filepath (str): The filepath to the json file.

        """
        with open(filepath, 'w') as jfile:
            json.dump(self.save_dict(), jfile, indent=4)

    def save_dict(self):
        """Returns a :class:`dict` of all configurations.

        Note:
            If a method ``_save_{config}`` exists, use that method to export
            this config.

        Returns:
            dict: The exported dict.

        """
        result = dict()
        for key in self._config:
            save = '_save_%s' % key
            if hasattr(self, save):
                value = getattr(self, save)()
            else:
                value = getattr(self, key)
            result[key] = value
        return result
