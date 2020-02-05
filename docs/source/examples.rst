Examples
========

1. Basic Usage
--------------

.. testcode::

   from singleton_config import Config

   # Inherit from Config for customized configurations
   class MyConfig(Config):
      def __init__(self):
          super().__init__() # call this at the first line
          self.add_config('a', 10)
          self.add_config('b', 20)

   config1 = MyConfig()
   config1.a = 0

   # Add new config via the method "add_config"
   config1.add_config('c', 30)
   print(config1)

.. testoutput::

    ------------------
    builtins.MyConfig:
        a: 0
        b: 20
        c: 30
    ------------------

.. testcode::

    config2 = MyConfig()
    # Singleton ensures that all the instances are the same
    print(config1 is config2)

.. testoutput::

   True


2. Save and Load
----------------

.. testcode:: 

   # Users can implement conversion functions for saving and loading a config
   class MyConfig(Config):
      def __init__(self):
          super().__init__() # call this at the first line
          self.add_config('a', 10)
          self.add_config('b', 20)
      def _save_a(self):
          return str(self.a)
      def _load_a(self, value):
          self.a = int(value)

   config = MyConfig()
   print(config.save_dict())

.. testoutput::

   {'a': '10', 'b': 20}

.. testcode::

   config.load_dict({'a': '100'})
   print(config.a, type(config.a))

.. testoutput:: 

   100 <class 'int'>

.. testcode::

   # Work with a json file
   config.save_json('config.json')
   config.load_json('config.json')
