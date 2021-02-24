#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 桜火, Inc. All Rights Reserved 
#
# @Time    : 2021/2/17 19:37
# @Author  : 桜火
# @Email   : xie@loli.fit
# @File    : data_process.py
# @Software: PyCharm
import time


def timestamp(time_num):
	_time_data = time.localtime(time_num)

	_result = (str(_time_data.tm_year) + "年" + str(_time_data.tm_mon) + "月" + str(_time_data.tm_mday) + "日" + str(
		_time_data.tm_hour) + "时" + str \
		           (_time_data.tm_min) + "分" + str(_time_data.tm_sec) + "秒")
	return _result
