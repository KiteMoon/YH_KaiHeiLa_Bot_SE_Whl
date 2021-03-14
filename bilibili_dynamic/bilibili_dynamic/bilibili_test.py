#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 桜火, Inc. All Rights Reserved 
#
# @Time    : 2021/2/26 13:37
# @Author  : 桜火
# @Email   : xie@loli.fit
# @File    : bilibili_test.py
# @Software: PyCharm
import requests
import json
import time
import datetime

headers = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.47 Safari/537.36 Edg/89.0.774.27",
	"Origin": "https://space.bilibili.com",
	"Sec-Fetch-Site": "same-site",
	"Sec-Fetch-Mode": "cors",
	"Sec-Fetch-Dest": "empty",
	"Referer": "https://space.bilibili.com/",
	"Cookie": "l=v; _uuid=030CF8B2-4699-D6F2-7D78-9F802EC997E562133infoc; buvid3=0BFE615D-9523-4B4E-90B4-94E385671EEE143094infoc; sid=jpvmhspz; DedeUserID=37958451; DedeUserID__ckMd5=58b01ed465ac1c5e; SESSDATA=79a3e1a3%2C1622035472%2C34146*b1; bili_jct=487a0cf4b755075012ddfb5adbf0e63d; CURRENT_FNVAL=80; blackside_state=1; rpdid=|(um)~uml)kY0J'uY|YR)JR)u; LIVE_BUVID=AUTO6916064885389528; buvid_fp_plain=0BFE615D-9523-4B4E-90B4-94E385671EEE143094infoc; buivd_fp=0BFE615D-9523-4B4E-90B4-94E385671EEE143094infoc; CURRENT_QUALITY=116; buvid_fp=0BFE615D-9523-4B4E-90B4-94E385671EEE143094infoc; balh_server_inner=__custom__; balh_is_closed=; bp_video_offset_37958451=484944087382561530; fingerprint3=e6a79e5e514e6988ff273238610536dc; fingerprint=dfc25dcb3c20694387f77bf16d4c3824; fingerprint_s=f6eeafeb2ff34f0a6e507e3c04aa4521; PVID=3; bp_t_offset_37958451=493414669132174862"
}


def time_num(time_str):
	_time_data = time.localtime(time_str)
	times = (str(_time_data.tm_year) + "年" + str(_time_data.tm_mon) + "月" + str(_time_data.tm_mday) + "日" + str(
		_time_data.tm_hour) + "时" + str \
		         (_time_data.tm_min) + "分" + str(_time_data.tm_sec) + "秒")  # 生成时间戳
	return times


def link_get(UID):
	_dynamic_url = "https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?visitor_uid=" + str(UID) + \
	               "&host_uid=" + str(UID) + "&offset_dynamic_id=0&need_top=1&platform=web"
	_bilibili_dynamic_get = requests.get(url=_dynamic_url, headers=headers)
	_bilibili_dynamic_get.status_code
	_bilibili_dynamic_get_json = _bilibili_dynamic_get.json()
	print(_dynamic_url)
	return _bilibili_dynamic_get_json


# --------------置顶算法------------------------------#
# if bilibili_dynamic_get_json["data"]["cards"][0]["extra"]["is_space_top"] == 1:
# 	print("这是置顶")
# --------------该字串为单独发文字动态使用---------------#
def bilibili_text_dynamic(bilibili_dynamic_get_json):
	if bilibili_dynamic_get_json["data"]["cards"][0]["extra"]["is_space_top"] == 1:
		num = 1
	else:
		num = 0

	bilibili_dynamic_desc = bilibili_dynamic_get_json["data"]["cards"][num]["desc"]
	print("该字串为单独发文字动态使用")
	bilibili_dynamic_result_all = bilibili_dynamic_get_json["data"]["cards"][num]["card"]  # 列表第一个索引是用户名，第二个是动态
	bilibili_dynamic_result_all = json.loads(bilibili_dynamic_result_all)
	print(bilibili_dynamic_result_all)
	bilibili_dynamic_name = bilibili_dynamic_get_json["data"]["cards"][num]["desc"]["user_profile"]["info"][
		"uname"]  # 稳定获取名称接口
	bilibili_dynamic_body = bilibili_dynamic_result_all["item"]["content"]  # 获取动态内容
	# print(bilibili_dynamic_name)
	# print(bilibili_dynamic_body)
	_content1 = "系统订阅的用户更新了\n" + "昵称:" + str(bilibili_dynamic_name) + "\nUID:" + str(
		bilibili_dynamic_result_all["user"]["uid"]) \
	            + "\n动态ID:" + str(bilibili_dynamic_desc["dynamic_id_str"]) \
	            + "\n简介" + str(bilibili_dynamic_desc["user_profile"]["sign"]) + "\n动态内容:\n" + str(bilibili_dynamic_body)
	print(_content1)
	_content2 = "**动态内容**:\n" + str(bilibili_dynamic_body)
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
						"content": _content1
					},
					"mode": "right",
					"accessory": {
						"type": "image",
						"src": str(bilibili_dynamic_desc["user_profile"]["info"]["face"]),
						"size": "lg"
					}
				},
				{
					"type": "divider"
				},
				{
					"type": "section",
					"text": {
						"type": "kmarkdown",
						"content": _content2
					}
				},
				{
					"type": "action-group",
					"elements": [
						{
							"type": "button",
							"theme": "primary",
							"value": "https://t.bilibili.com/" + str(
								bilibili_dynamic_desc["dynamic_id_str"]) + "?tab=2",
							"click": "link",
							"text": {
								"type": "plain-text",
								"content": "跳转到原动态"
							}
						}
					]
				}
			]
		}
	]
	# print(card_view)
	_result = (json.dumps(card_view, ensure_ascii=False))
	return _result


# --------------该字串为发布视频动态使用，正常运行，需要UID---------------#
def bilibili_video_dynamic(bilibili_dynamic_get_json):
	print("loli")
	if bilibili_dynamic_get_json["data"]["cards"][0]["extra"]["is_space_top"] == 1:
		num = 1
	else:
		num = 0
	bilibili_dynamic_desc = bilibili_dynamic_get_json["data"]["cards"][num]["desc"]
	print("该字串为发布视频动态使用，正常运行，需要UID")
	bilibili_dynamic_result_all = bilibili_dynamic_get_json["data"]["cards"][num]["card"]
	bilibili_dynamic_result_all = json.loads(bilibili_dynamic_result_all)
	bilibili_dynamic_name = bilibili_dynamic_get_json["data"]["cards"][num]["desc"]["user_profile"]["info"][
		"uname"]  # 昵称
	# (print(bilibili_dynamic_result_all))
	bilibili_dynamic_aid = bilibili_dynamic_result_all["aid"]  # 视频AV号
	bilibili_dynamic_title = bilibili_dynamic_result_all["title"]  # 标题
	bilibili_dynamic_img = bilibili_dynamic_result_all["pic"]  # 图片链接
	bilibili_dynamic_info = bilibili_dynamic_result_all["desc"]  # 简介
	# print(bilibili_dynamic_name)
	# print(bilibili_dynamic_title)
	# print(bilibili_dynamic_aid)
	# print(bilibili_dynamic_img)
	# print(bilibili_dynamic_info)
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
						"content": "用户订阅的UP主：" + bilibili_dynamic_name + "更新了视频"
					}
				},
				{
					"type": "section",
					"text": {
						"type": "plain-text",
						"content": "视频名称:" + str(bilibili_dynamic_title) + "\n作者:" + str(
							bilibili_dynamic_name) + "\n简介:" + bilibili_dynamic_info
					}
				},
				{
					"type": "image-group",
					"elements": [
						{
							"type": "image",
							"src": bilibili_dynamic_img
						}
					]
				},
				{
					"type": "action-group",
					"elements": [
						{
							"type": "button",
							"theme": "primary",
							"value": "https://www.bilibili.com/video/av" + str(bilibili_dynamic_aid),
							"click": "link",
							"text": {
								"type": "plain-text",
								"content": "跳转到视频"
							}
						}
					]
				}
			]
		}
	]
	_result = (json.dumps(card_view, ensure_ascii=False))

	return _result


# --------------该字串为图片+文字动态/也可以单独图片使用---------------#
def bilibili_png_dynamic(bilibili_dynamic_get_json):
	if bilibili_dynamic_get_json["data"]["cards"][0]["extra"]["is_space_top"] == 1:
		num = 1
	else:
		num = 0
	print("该字串为图片+文字动态/也可以单独图片使用")
	bilibili_dynamic_result_all = bilibili_dynamic_get_json["data"]["cards"][num]["card"]
	bilibili_dynamic_result_all = json.loads(bilibili_dynamic_result_all)
	bilibili_dynamic_name = bilibili_dynamic_get_json["data"]["cards"][num]["desc"]["user_profile"]["info"][
		"uname"]  # 昵称
	bilibili_dynamic_body = bilibili_dynamic_result_all["item"]["description"]  # 动态内容
	bilibili_dynamic_img = bilibili_dynamic_result_all["item"]["pictures"]  # 动态图片，需要for
	print(bilibili_dynamic_name)
	print(bilibili_dynamic_body)
	img_num = (len(bilibili_dynamic_img))
	print(img_num)
	_elements = []
	for num in range(0, (img_num)):  # 这里用于生成多图动态的图片部分
		element = {
			"type": "image",
			"src": bilibili_dynamic_img[num]["img_src"]
		}
		_elements.append(element)
	print(_elements)
	bilibili_dynamic_desc = bilibili_dynamic_get_json["data"]["cards"][num]["desc"]
	times = time_num(bilibili_dynamic_desc["timestamp"])
	card_view = [
		{
			"type": "card",
			"theme": "secondary",
			"size": "lg",
			"modules": [
				{
					"type": "section",
					"text": {
						"type": "kmarkdown",
						"content": "**您关注的用户:" + bilibili_dynamic_desc["user_profile"]["info"]["uname"] + "更新了动态**"
					}
				},
				{
					"type": "context",
					"elements": [
						{
							"type": "image",
							"src": str(bilibili_dynamic_desc["user_profile"]["info"]["face"])
						},
						{

							"type": "kmarkdown",
							"content": "**{}**    {}".format(bilibili_dynamic_desc["user_profile"]["info"]["uname"], \
							                                 times)
						}
					]
				},
				{
					"type": "section",
					"text": {
						"type": "kmarkdown",
						"content": "**动态内容:**\n" + bilibili_dynamic_body
					}
				},
				{
					"type": "image-group",
					"elements": _elements
				}
			]
		}
	]
	_result = json.dumps(card_view)
	return (_result)


# --------------该字串转发视频使用,正常运行，需要UID---------------#
def bilibili_share_video_dynamic(bilibili_dynamic_get_json):
	if bilibili_dynamic_get_json["data"]["cards"][0]["extra"]["is_space_top"] == 1:
		num = 1
	else:
		num = 0
	print("进入转发视频")
	print("下方为接收的数据")
	print(bilibili_dynamic_get_json)
	bilibili_dynamic_result_all = bilibili_dynamic_get_json["data"]["cards"][num]["card"]  # 列表第一个索引是用户名，第二个是动态
	bilibili_dynamic_result_all = json.loads(bilibili_dynamic_result_all)
	bilibili_dynamic_name = bilibili_dynamic_get_json["data"]["cards"][num]["desc"]["user_profile"]["info"][
		"uname"]  # 稳定获取名称接口
	bilibili_dynamic_body = bilibili_dynamic_result_all["item"]["content"]  # 获取动态内容
	bilibili_dynamic_video_origin = json.loads(bilibili_dynamic_result_all["origin"])  # 获取动态内容
	bilibili_dynamic_video_aid = bilibili_dynamic_video_origin["aid"]  # 转发的AV号
	bilibili_dynamic_video_title = bilibili_dynamic_video_origin["title"]  # 转发视频的标题
	bilibili_dynamic_video_name = bilibili_dynamic_video_origin["owner"]["name"]
	bilibili_dynamic_video_pic = bilibili_dynamic_video_origin["pic"]
	bilibili_dynamic_video_introduction = bilibili_dynamic_video_origin["desc"]  # 转发的视频的简介
	print(bilibili_dynamic_name)
	print(bilibili_dynamic_body)
	print(bilibili_dynamic_video_aid)
	print(bilibili_dynamic_video_title)
	print(bilibili_dynamic_video_introduction)
	print(bilibili_dynamic_video_pic)
	bilibili_dynamic_desc = bilibili_dynamic_get_json["data"]["cards"][num]["desc"]
	share_time = time_num(bilibili_dynamic_desc["timestamp"])
	card_view = [
		{
			"type": "card",
			"theme": "secondary",
			"size": "lg",
			"modules": [
				{
					"type": "section",
					"text": {
						"type": "kmarkdown",
						"content": "**您关注的用户:{}更新了动态**".format(bilibili_dynamic_name)
					}
				},
				{
					"type": "divider"
				},
				{
					"type": "context",
					"elements": [
						{
							"type": "image",
							"src": bilibili_dynamic_desc["user_profile"]["info"]["face"]
						},
						{
							"type": "kmarkdown",
							"content": "**{}**    {}".format(bilibili_dynamic_name, share_time)
						}
					]
				},
				{
					"type": "section",
					"text": {
						"type": "kmarkdown",
						"content": "**源动态:**\n" + bilibili_dynamic_body
					}
				},
				{
					"type": "divider"
				},
				{
					"type": "context",
					"elements": [
						{
							"type": "image",
							"src": bilibili_dynamic_video_origin["pic"]
						},
						{
							"type": "plain-text",
							"content": bilibili_dynamic_video_name + "    发布的视频\t" + time_num(
								bilibili_dynamic_video_origin["pubdate"])
						}
					]
				},
				{
					"type": "section",
					"text": {
						"type": "plain-text",
						"content": "视频名称:" + bilibili_dynamic_video_title + "\n作者:" + bilibili_dynamic_video_name + "\n简介:" + bilibili_dynamic_video_introduction
					}
				},
				{
					"type": "image-group",
					"elements": [
						{
							"type": "image",
							"src": str(bilibili_dynamic_video_pic)
						}
					]
				},
				{
					"type": "action-group",
					"elements": [
						{
							"type": "button",
							"theme": "primary",
							"value": "https://www.bilibili.com/video/av" + str(bilibili_dynamic_video_aid),
							"click": "link",
							"text": {
								"type": "plain-text",
								"content": "跳转到视频"
							}
						}
					]
				}
			]
		}
	]
	print(json.dumps(card_view, ensure_ascii=False))


# -----------该字段用于转发图片+动态使用,正常运行，需要UID---------#
def bilibili_share_png_dynamic(bilibili_dynamic_get_json):
	if bilibili_dynamic_get_json["data"]["cards"][0]["extra"]["is_space_top"] == 1:
		num = 1
	else:
		num = 0
	bilibili_dynamic_result_all = bilibili_dynamic_get_json["data"]["cards"][num]["card"]  # 列表第一个索引是用户名，第二个是动态
	bilibili_dynamic_result_all_json = json.loads(bilibili_dynamic_result_all)
	bilibili_dynamic_desc = bilibili_dynamic_get_json["data"]["cards"][num]["desc"]
	# print(bilibili_dynamic_result_all_json["user"]["uname"])  # 转发人的名称
	# print(bilibili_dynamic_result_all_json["item"]["content"])  # 转发人转发动态的蚊子
	bilibili_dynamic_result_origin_json = json.loads(bilibili_dynamic_result_all_json["origin"])
	# print(bilibili_dynamic_result_origin_json["item"]["description"])  # 转发的动态主体文字
	# -------下面这个部分用于生成多图代码------#
	img_num = (len(bilibili_dynamic_result_origin_json["item"]["pictures"]))
	img_list = (bilibili_dynamic_result_origin_json["item"]["pictures"])
	_elements = []
	_de_elements = []
	times = time_num(bilibili_dynamic_desc["timestamp"])
	for num in range(0, (img_num)):  # 这里用于生成多图动态的图片部分
		_img_url = ""
		_img_url = (img_list[num]["img_src"]) + "@320w_267h_1e_1c.jpg"
		element = {
			"type": "image",
			"src": _img_url
		}
		_elements.append(element)
	# -------下面这个部分用于生成卡片模板------#
	card_view = [
		{
			"type": "card",
			"theme": "secondary",
			"size": "lg",
			"modules": [
				{
					"type": "section",
					"text": {
						"type": "kmarkdown",
						"content": "**您关注的用户:" + bilibili_dynamic_result_all_json["user"]["uname"] + "更新了动态**"
					}
				},
				{
					"type": "divider"
				},
				{
					"type": "context",
					"elements": [
						{
							"type": "image",
							"src": str(bilibili_dynamic_desc["user_profile"]["info"]["face"])
						},
						{

							"type": "kmarkdown",
							"content": "**{}**    {}".format(bilibili_dynamic_result_all_json["user"]["uname"], \
							                                 times)
						}
					]
				},
				{
					"type": "section",
					"text": {
						"type": "kmarkdown",
						"content": "**源动态:**\n" + str(bilibili_dynamic_result_all_json["item"]["content"])
					}
				},
				{
					"type": "divider"
				},
				{
					"type": "section",
					"text": {
						"type": "kmarkdown",
						"content": "**转发动态:**\n" + bilibili_dynamic_result_origin_json["item"]["description"]
					}
				},
				{
					"type": "image-group",
					"elements": _elements
				}
			]
		}
	]
	_result = json.dumps(card_view, ensure_ascii=False)
	print(_result)
	return _result


def bilibili_share_text_dynamic(bilibili_dynamic_get_json):
	if bilibili_dynamic_get_json["data"]["cards"][0]["extra"]["is_space_top"] == 1:
		num = 1
	else:
		num = 0
	bilibili_dynamic_result_all = bilibili_dynamic_get_json["data"]["cards"][num]["card"]  # 列表第一个索引是用户名，第二个是动态
	bilibili_dynamic_result_info = bilibili_dynamic_get_json["data"]["cards"][num]  # 列表第一个索引是用户名，第二个是动态
	bilibili_dynamic_result_all_json = json.loads(bilibili_dynamic_result_all)

	# print(bilibili_dynamic_result_all_json["user"]["uname"])  # 转发人的名称
	# print(bilibili_dynamic_result_all_json["item"]["content"])  # 转发人转发动态的蚊子
	bilibili_dynamic_result_origin_json = json.loads(bilibili_dynamic_result_all_json["origin"])

	print(bilibili_dynamic_result_origin_json["item"]["content"])  # 转发的动态主体文字
	card_view = [
		{
			"type": "card",
			"theme": "secondary",
			"size": "lg",
			"modules": [
				{
					"type": "section",
					"text": {
						"type": "kmarkdown",
						"content": "系统关注的UP主{} 转发动态".format(
							bilibili_dynamic_result_info["desc"]["user_profile"]["info"]["uname"])
					}
				},
				{
					"type": "context",
					"elements": [
						{
							"type": "image",
							"src": bilibili_dynamic_result_info["desc"]["user_profile"]["info"]["face"]
						},
						{
							"type": "plain-text",
							"content": str(bilibili_dynamic_result_all_json["user"]["uname"])
						}
					]
				},
				{
					"type": "section",
					"text": {
						"type": "kmarkdown",
						"content": str(bilibili_dynamic_result_origin_json["item"]["content"])
					}
				},
				{
					"type": "divider"
				},
				{
					"type": "context",
					"elements": [
						{
							"type": "image",
							"src":"www.baidu.com"
						},
						{
							"type": "plain-text",
							"content": "XXXS"
						}
					]
				},
				{
					"type": "section",
					"text": {
						"type": "kmarkdown",
						"content": "动态内容"
					}
				}
			]
		}
	]
	print(json.dumps(card_view))

def bilibili_dynamic(target_id, card_view, UID, quote="", nonce="", temp_target_id=""):
	bilibili_dynamic_get_json = link_get(UID)
	# bilibili_video_dynamic(bilibili_dynamic_get_json)
	# bilibili_png_dynamic(bilibili_dynamic_get_json)
	# print(bilibili_dynamic_get_json)
	return (ccc(bilibili_dynamic_get_json))


def ccc(bilibili_dynamic_get_json):
	if bilibili_dynamic_get_json["data"]["cards"][0]["extra"]["is_space_top"] == 1:
		num = 1
	else:
		num = 0
	print(num)
	bilibili_dynamic_get_json_card = json.loads(bilibili_dynamic_get_json["data"]["cards"][num]["card"])
	print("type")
	print(bilibili_dynamic_get_json["data"]["cards"][num]["desc"]["type"])
	# print(bilibili_dynamic_get_json)
	del bilibili_dynamic_get_json["data"]["attentions"]
	print(bilibili_dynamic_get_json)
	print((bilibili_dynamic_get_json_card))
	# 这里用于执行除转发的动态
	if bilibili_dynamic_get_json["data"]["cards"][num]["desc"]["type"] == 1:
		# print("这是一个转发类动态")  # 识别是转发视频还是播放视频
		# print(bilibili_dynamic_get_json["data"]["cards"][num]["desc"]["origin"])
		_bilibili_dynamic_type = bilibili_dynamic_get_json["data"]["cards"][num]["desc"]["origin"]["type"]
		# print(_bilibili_dynamic_type)
		if _bilibili_dynamic_type == 2:  # 逻辑判断，转发图片
			# print(bilibili_dynamic_get_json["data"]["cards"][num]["card"])
			# print("hello")
			return (bilibili_share_png_dynamic(bilibili_dynamic_get_json))
		elif _bilibili_dynamic_type == 8:  # 逻辑判断，转发视频
			print("rush")
			bilibili_share_video_dynamic(bilibili_dynamic_get_json)
		elif _bilibili_dynamic_type == 4:  # 逻辑判断，转发文字
			print("gogogo")
			bilibili_share_text_dynamic(bilibili_dynamic_get_json)
	# 这里用于执行除转发之外的动态
	elif "bvid" in bilibili_dynamic_get_json["data"]["cards"][num]["desc"]:
		# print(type(bilibili_dynamic_get_json["data"]["cards"][num]["card"]))
		print("这是一个视频动态")  # 识别是转发视频还是播放视频
		return (bilibili_video_dynamic(bilibili_dynamic_get_json))
	elif bilibili_dynamic_get_json["data"]["cards"][num]["desc"]["type"] == 4:
		print("检测到文字")
		return (bilibili_text_dynamic(bilibili_dynamic_get_json))
	elif bilibili_dynamic_get_json["data"]["cards"][num]["desc"]["type"] == 2:
		print("检测到图片+文字")
		print(bilibili_png_dynamic(bilibili_dynamic_get_json))
		return (bilibili_png_dynamic(bilibili_dynamic_get_json))
	print(bilibili_dynamic_get_json)


# bilibili_share_text_dynamic(bilibili_dynamic_get_json)
# print(bilibili_dynamic_get_json)
# print("这是转发视频动态态")
# (bilibili_dynamic("1","1","2863937"))
# print("转发动态")
# print(bilibili_dynamic("1", "1", "38453374"))
#
# print("-----------------------")
# print("这是视频动态")
# print(bilibili_dynamic("1", "1", "18149131"))
# print("-----------------------")
# print("这是文字")
# print(bilibili_dynamic("1", "1", "37958451"))
# print("这是文字+图片直发")
# print(bilibili_dynamic("1", "1", "928123"))
# print("-----------分享图片------------")
print(bilibili_dynamic("1", "1", "37958451"))
