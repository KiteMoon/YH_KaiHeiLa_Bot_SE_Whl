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
setup(name='bilibili_video',
   version='0.1.4',
   description='YH_kaiheila_SE rely,Realize bilibili video data acquisition',
   author='Ying_Huo',
   author_email='xie@loli.fit',
   url='https://blog.loli.fit/',
   license='MIT',
   keywords='YH KHL',
   packages=['bilibili_video'],
   install_requires=['requests>=2.25.1'],
   python_requires='>=3'
   )