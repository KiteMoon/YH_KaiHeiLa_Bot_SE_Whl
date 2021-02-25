#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 桜火, Inc. All Rights Reserved 
#
# @Time    : 2021/2/22 20:33
# @Author  : 桜火
# @Email   : xie@loli.fit
# @File    : setup.py
# @Software: PyCharm
from setuptools import setup
setup(name='rainbow_six_find',
      version='1.0.5',
      description='rainbow_six_find',
      author='YingHuo',
      author_email='xie@loli.fit',
      url='https://blog.loli.fit',
      license='MIT',
      keywords='YH KHL',
      packages=['rainbow_six'],
      install_requires=['requests>=2.25.1'],
      python_requires='>=3'
      )
