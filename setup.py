# -*- coding: utf-8 -*-

from distutils.core import setup
import subprocess

command = ['git', 'describe', '--tags']
version = subprocess.check_output(command).decode().strip()

setup(name='config',
      version=version,
      description='Global configurations with singleton design pattern.',
      author='Shuo Han',
      author_email='shan50@jhu.edu',
      packages=['singleton_config'])
