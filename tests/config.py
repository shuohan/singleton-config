#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from singleton_config import Config as Config_


class Config(Config_):
    def __init__(self):
        super().__init__()
        self.add_config('a', 1)
        self.add_config('b', '2')

    def _save_a(self):
        return str(self.a)

    def _load_a(self, value):
        self.a = int(value)


def test_config():
    config1 = Config()
    assert config1.a == 1
    assert config1.b == '2'
    try:
        config1.c = 10
        assert False
    except RuntimeError:
        assert True
    config1.a = 100

    config2 = Config()
    assert config2.a == 100
    assert id(config1) == id(config2)

    print(config2)
    heading = '%s.Config:' % __name__
    message = '\n'.join([heading,
                         '    a: 100',
                         '    b: 2'])
    assert config1.__str__() == message

    filename = 'test.json'
    config2.save_json(filename)

    config2.a = 1
    config3 = Config()
    assert id(config2) == id(config3)
    config3.add_config('c', 'hello world')
    assert config2.save_dict() == {'a': "1", 'b': '2', 'c': 'hello world'}

    with open(filename) as jfile:
        lines = jfile.readlines()
    assert lines == ['{\n', '    "a": "100",\n', '    "b": "2"\n', '}']

    assert config1.a == 1
    config1.load_json(filename)
    assert config1.a == 100
    assert config1.b == '2'
    assert config1.c == 'hello world'

    os.remove(filename)
    print('all successful')


if __name__ == "__main__":
    test_config()
