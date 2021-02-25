#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 桜火, Inc. All Rights Reserved 
#
# @Time    : 2021/2/22 22:26
# @Author  : 桜火
# @Email   : xie@loli.fit
# @File    : KHL_POST_TEXT_MOD.py
# @Software: PyCharm
import requests
import configparser
import os
import json
# 获取机器人key信息，以便发起GET操作
def post_kaiheila_message(type,target_id,card_view,quote="",nonce="",temp_target_id=""):  # 发送聊天消息
	config_info = configparser.ConfigParser()
	fui = config_info.read("config.ini")
	Authorization = config_info.get("kaiheila", "websockt_token")
	DEV_MODE = config_info.get("DEV", "MODE")
	print("开发者模式：" + str(DEV_MODE))
	# 初始化配置文件
	message_data = {
		"type":type,
		"target_id":target_id,
		"content":json.dumps(card_view, ensure_ascii=False),
		"nonce":nonce,
		"quote":quote,
		"temp_target_id":temp_target_id
	}
	#生成将要被POST的对象
	headers = {
		"Authorization": Authorization
	}
	_post_message_url = "https://www.kaiheila.cn/api/v3/channel/message"
	_post_kaiheila_message_requests = requests.post(url=_post_message_url, headers=headers,
	                                                data=message_data)
	#发出POST请求，这里到底要不要转json啊
	if DEV_MODE == "1":
		print("密钥为" + Authorization)
		print(headers)
	print(_post_kaiheila_message_requests.text)
	#开发模式用