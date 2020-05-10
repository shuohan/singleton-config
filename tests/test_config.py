#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from enum import IntEnum

from singleton_config import Config as Config_


class Mode(IntEnum):
    M1 = 1
    M2 = 2


class Config(Config_):
    def __init__(self):
        super().__init__()
        self.add_config('a', 1)
        self.add_config('b', '2')
        self.add_config('cc', Mode.M1, True)

    def _save_a(self):
        return str(self.a)

    def _load_a(self, value):
        self.a = int(value)

    @property
    def cc(self):
        return self._cc

    @cc.setter
    def cc(self, mode):
        if isinstance(mode, Mode):
            self._cc = mode
        elif isinstance(mode, int):
            self._cc = Mode(mode)
        elif isinstance(mode, str):
            self._cc = Mode[mode]


def test_config():
    config1 = Config()
    assert config1.a == 1
    assert config1.b == '2'
    assert config1.cc is Mode.M1
    assert config1.has_config('cc')
    try:
        config1.d = 10
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
                         '     a: 100',
                         '     b: 2',
                         '    cc: Mode.M1'])
    assert config1.__str__() == message

    filename = 'test.json'
    config2.cc = Mode.M2
    config2.save_json(filename)

    config2.a = 1
    config3 = Config()
    assert id(config2) == id(config3)
    config3.add_config('d', 'hello world')
    tmp = {'a': '1', 'b': '2', 'cc': Mode.M2, 'd': 'hello world'}
    assert config2.save_dict() == tmp

    with open(filename) as jfile:
        lines = jfile.readlines()
    tmp = ['{\n', '    "a": "100",\n','    "b": "2",\n', '    "cc": 2\n', '}']
    assert lines == tmp

    assert config1.a == 1
    config1.load_json(filename)
    assert config1.a == 100
    assert config1.b == '2'
    assert config1.cc is Mode.M2
    assert config1.d == 'hello world'

    os.remove(filename)
    print('all successful')


if __name__ == '__main__':
    test_config()
