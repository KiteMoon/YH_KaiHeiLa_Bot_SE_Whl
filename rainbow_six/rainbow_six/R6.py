#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 桜火, Inc. All Rights Reserved 
#
# @Time    : 2021/2/24 21:41
# @Author  : 桜火
# @Email   : xie@loli.fit
# @File    : R6.py
# @Software: PyCharm
import json
import re
import requests
def get_r6_Foundation_info(message_text, target_id):
	print("进入彩虹六号处理视图层")
	name = message_text
	_get_tendai_card_url = "https://www.r6s.cn/v2/stats/index?username=" + name
	_headers = {
		"referer": "https://www.r6s.cn/stats.jsp?username=" + name,
		"sec-fetch-dest": "empty",
		"sec-fetch-mode": "cors",
		"sec-fetch-site": "same-origin",
		"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ""Chrome/89.0.4389.47 Safari/537.36 Edg/89.0.774.27 "
	}
	_get_tendai_card_json = requests.get(url=_get_tendai_card_url, headers=_headers).json()
	user_id = str(_get_tendai_card_json["Basicstat"][0]["user_id"])
	print(type(_get_tendai_card_json))
	print(_get_tendai_card_json["Basicstat"])
	#获取数据
	content = "名称：" + name + \
	          "\n唯一ID：" + str(_get_tendai_card_json["Basicstat"][0]["user_id"]) + \
	          "\n等级：" + str(_get_tendai_card_json["Basicstat"][0]["level"]) + \
	          "\n当前赛季最高MMR：" + str(_get_tendai_card_json["Basicstat"][0]["mmr"]) + \
	          "\n当前赛季胜场数：" + str(_get_tendai_card_json["Basicstat"][0]["wins"]) + \
	          "\n当前赛季败场数：" + str(_get_tendai_card_json["Basicstat"][0]["losses"]) + \
	          "\n购买游戏时间：" + str(_get_tendai_card_json["Basicstat"][0]["updated_at"]) + \
	          "\n当前赛季击杀数：" + str(_get_tendai_card_json["Basicstat"][0]["kills"]) + \
	          "\n当前赛季死亡数：" + str(_get_tendai_card_json["Basicstat"][0]["deaths"])
	print(content)
	card_view = [
		{
			"type": "card",
			"theme": "secondary",
			"size": "lg",
			"modules": [
				{
					"type": "section",
					"text": {
						"type": "plain-text",
						"content": content
					},
					"mode": "right",
					"accessory": {
						"type": "image",
						"src": "https://ubisoft-avatars.akamaized.net/" + user_id + "/default_146_146.png",
						"size": "lg"
					}
				}
			]
		}
	]#生成消息
	message_data = {
		"type": "10",
		"target_id": str(target_id),
		"card_view": card_view
	}
	return message_data