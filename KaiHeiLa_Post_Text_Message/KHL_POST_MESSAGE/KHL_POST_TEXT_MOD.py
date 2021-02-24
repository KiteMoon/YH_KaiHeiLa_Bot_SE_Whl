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
def post_kaiheila_message(data):  # 发送聊天消息
	config_info = configparser.ConfigParser()
	fui = config_info.read("config.ini")
	Authorization = config_info.get("kaiheila", "websockt_token")
	DEV_MODE = config_info.get("DEV", "MODE")
	print("开发者模式：" + str(DEV_MODE))
	# 初始化配置文件
	card_message_data = {
		"type": str(data['type']),
		"channel_id": str(data['target_id']),
		"content": json.dumps(data["card_view"])
	}
	headers = {
		"Authorization": Authorization
	}
	message_data = json.dumps(card_message_data)
	_post_message_url = "https://www.kaiheila.cn/api/v3/channel/message"
	_post_kaiheila_message_requests = requests.post(url=_post_message_url, headers=headers,
	                                                data=card_message_data)
	if DEV_MODE == "1":
		print("密钥为" + Authorization)
		headers
	print(_post_kaiheila_message_requests.text)
