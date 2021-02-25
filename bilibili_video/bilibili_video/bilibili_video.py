#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 桜火, Inc. All Rights Reserved 
#
# @Time    : 2021/2/17 13:39
# @Author  : 桜火
# @Email   : xie@loli.fit
# @File    : bilibili_video.py
# @Software: PyCharm
import requests
import time
import json
from .data_process import timestamp
import configparser
import os

config_info = configparser.ConfigParser()
fui = config_info.read("config.ini")
DEV_MODE = config_info.get("DEV", "MODE")
print("开发者模式：" + str(DEV_MODE))
headers = {
	"Connection": "keep-alive",
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.47 Safari/537.36 Edg/89.0.774.27",
	"Accept": "*/*",
	"Sec-Fetch-Site": "same-origin",
	"Sec-Fetch-Mode": "cors",
	"Sec-Fetch-Dest": "empty",
	"Referer": "https://www.bilibili.com/",
	"Accept-Encoding": "gzip, deflate, br",
	"Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
}


def get_video_player(aid):  # 通过AID获取播放量，已经弃用
	_url_aid = "http://api.bilibili.com/archive_stat/stat?aid=" + str(aid) + "&type=jsonp"
	_video_player = requests.get(url=_url_aid, headers=headers)
	_video_player_json = _video_player.json()
	if DEV_MODE == "1":
		print("---下方为B站API AID返回信息---")
		print(_video_player_json)
	return _video_player_json


def get_video_info(bvid):  # 获取B站API中包含的数据
	_url_bid = "https://api.bilibili.com/x/web-interface/view?bvid=" + bvid
	_video_info = requests.get(url=_url_bid, headers=headers)
	_video_info_json = _video_info.json()
	if DEV_MODE == "1":
		print("---下方为B站API BID返回信息---")
		print(_video_info_json)
	return _video_info_json


def time_list(time_num):  # 下个版本删了
	time_data = time.localtime(time_num)


def _result_bilibili_video_info(bvid, target_id):
	print("=========BILIBILI视频解析模块开始运行=========")
	print("接收BV号：" + str(target_id))
	print("接收消息房间ID：" + str(target_id))
	_video_info_json = get_video_info(bvid)  # 调用方法获取信息
	if _video_info_json["code"] == 0:  # 检测状态码，如果状态为0则识别为正常消息

		_video_info_player = get_video_player(_video_info_json["data"]["aid"])  # 获取AV号，这里如果想要提高消息效率，可以把下面的aid删了
		# _result_disc = {
		#     "title": _video_info_json["data"]["title"],
		#     "pic": _video_info_json["data"]["pic"],
		#     "author": _video_info_json["data"]["owner"]["name"],
		#     "author_id": _video_info_json["data"]["owner"]["mid"],
		#     "aid": _video_info_json["data"]["aid"],
		#     "desc": _video_info_json["data"]["desc"],
		#     "time": timestamp(_video_info_json["data"]["ctime"]),
		# }
		# 下个版本删了。字符串拼串无需这个
		content = "视频名称：" + _video_info_json["data"]["title"] + "\n视频作者：" + _video_info_json["data"]["owner"]["name"] \
		          + "\n分区：" + _video_info_json["data"]["tname"] + "\n视频AV号：" + str(
			_video_info_json["data"]["aid"]) + "\n视频发布时间：" \
		          + str(timestamp(_video_info_json["data"]["ctime"])) + "\n视频播放量：" + str(
			_video_info_json["data"]["stat"]["view"]) \
		          + "\n视频点赞量：" + str(_video_info_json["data"]["stat"]["like"]) + "\n视频硬币数：" + str(
			_video_info_json["data"]["stat"]["coin"]) \
		          + "\n视频分享量：" + str(_video_info_json["data"]["stat"]["share"]) + "\n视频收藏量：" + str(
			_video_info_json["data"]["stat"]["favorite"]) \
		          + "\n视频弹幕数：" + str(_video_info_json["data"]["stat"]["danmaku"])

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
							"src": _video_info_json["data"]["pic"],
							"size": "lg"
						}
					},
					{
						"type": "action-group",
						"elements": [
							{
								"type": "button",
								"theme": "primary",
								"value": "https://www.bilibili.com/video/av" + str(_video_info_json["data"]["aid"]),
								"click": "link",
								"text": {
									"type": "plain-text",
									"content": "前往视频地址"
								}
							},
							{
								"type": "button",
								"theme": "danger",
								"value": _video_info_json["data"]["pic"],
								"click": "link",
								"text": {
									"type": "plain-text",
									"content": "获取封面"
								}
							}
						]
					}
				]
			}
		]  # 生成消息卡片样式，该样式只包含content，并且不会进行json解析，需要传参到message_data转义

		# message_data = {
		# 	"type": "10",
		# 	"channel_id": str(target_id),
		# 	"content": json.dumps(card_view)
		# }
		# 弃用，，改用统一编码接口
		_result = {
			"type": "10",
			"target_id": target_id,
			"card_view": json.dumps(card_view)}
		if DEV_MODE == "1":
			print("---开发模式---")
			print("---下方为卡片样式初始数据（未json）---")
			print(card_view)
			print("---下方为文字数据（未json）---")
			print(content)
			print("---下方为最终返回数据---")
			print(_result)
		else:
			print("已经生成card_view")
		print("已经返回请求信息")
		return (_result)
	else:
		print("发生错误")
		return ("error")  # 如果收到无法识别的消息，将会回传ERROR


if __name__ == '__main__':
	print("本函数是模块的一部分，不允许单独启用")
