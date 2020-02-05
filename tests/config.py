#!/usr/bin/env python
# -*- coding: utf-8 -*-

from singleton_config import Config as Config_


class Config(Config_):
    def __init__(self):
        super().__init__()
        self.add_config('a', 1)
        self.add_config('b', '2')


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
    print('all successful')



if __name__ == "__main__":
    test_config()
