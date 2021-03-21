#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 桜火, Inc. All Rights Reserved 
#
# @Time    : 2021/3/20 18:53
# @Author  : 桜火
# @Email   : xie@loli.fit
# @File    : bilibili_live.py
# @Software: PyCharm
import requests
import pymysql
import json
import configparser
import time
import random
config_info = configparser.ConfigParser()
fui = config_info.read("config.ini")
mysql_info_host = config_info.get("mysql","host")
mysql_info_name = config_info.get("mysql","db_name")
mysql_info_username = config_info.get("mysql","username")
mysql_info_password = config_info.get("mysql","password")
db = pymysql.connect(host=mysql_info_host, user=mysql_info_username, password=mysql_info_password, database=mysql_info_name)
cursor = db.cursor()
bot_header = {
	"Authorization":"Bot 1/MTAxNjA=/ugnbLazYqwKY8+wFl+65gA=="
}

def bilibili_live(UID):
	bilibili_url = "https://api.bilibili.com/x/space/acc/info?mid=" + str(UID) + "&jsonp=jsonp"
	#print(bilibili_url)
	headers = {
		"origin": "https://space.bilibili.com",
		"referer": "https://space.bilibili.com/",
		"sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"90\", \"Microsoft Edge\";v=\"90\"",
		"sec-ch-ua-mobile": "?0",
		"sec-fetch-dest": "empty",
		"sec-fetch-mode": "cors",
		"sec-fetch-site": "same-site",
		"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.19 Safari/537.36 Edg/90.0.818.8"
	}
	bilibili_live_all = (requests.get(url=bilibili_url, headers=headers))
	bilibili_live_json = bilibili_live_all.json()

	if bilibili_live_json["code"] == -404:
		print("error,没有找到这个UP")
		return {"code": "404"}
	if str(bilibili_live_json["data"]["live_room"]["liveStatus"])=="0":
		_sql = "UPDATE BILIBILI_LIVE SET LIVE_TYPE = 0 WHERE UID = {}".format(UID)
		#print(_sql)
		cursor.execute(_sql)
		db.commit()
		print("检测到主播并未开播，操作数据库成功")

	return {
		"code":"200",
		"name": (bilibili_live_json["data"]["name"]),
		"face_img": (str(bilibili_live_json["data"]["face"])),
		"live_type": (str(bilibili_live_json["data"]["live_room"]["liveStatus"])),
		"live_title": (str(bilibili_live_json["data"]["live_room"]["title"])),
		"live_room_id": (str(bilibili_live_json["data"]["live_room"]["roomid"])),
		"live_online": (str(bilibili_live_json["data"]["live_room"]["online"])),
		"live_url": (str(bilibili_live_json["data"]["live_room"]["url"])),
		"live_cover_img": (str(bilibili_live_json["data"]["live_room"]["cover"]))
	}
def cardview_post(UID):
	live_all = (bilibili_live(UID))
	_sql_find = "SELECT LIVE_TYPE FROM BILIBILI_LIVE WHERE UID={}".format(UID)
	cursor.execute(_sql_find)
	UID_live_type = cursor.fetchall()

	UID_live_type =(UID_live_type[0][0])
	if live_all["code"] == "200":
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
							"content": "**系统检测到新的直播动态**"
						}
					},
					{
						"type": "context",
						"elements": [
							{
								"type": "image",
								"src": live_all["face_img"]
							},
							{
								"type": "plain-text",
								"content": live_all["name"]
							}
						]
					},
					{
						"type": "image-group",
						"elements": [
							{
								"type": "image",
								"src": live_all["live_cover_img"]
							}
						]
					},
					{
						"type": "section",
						"text": {
							"type": "paragraph",
							"cols": 3,
							"fields": [
								{
									"type": "kmarkdown",
									"content": "**标题**\n{}".format(live_all["live_title"])
								},
								{
									"type": "kmarkdown",
									"content": "**观看人数**\n{}".format(live_all["live_online"])
								},
								{
									"type": "kmarkdown",
									"content": "**房间号**\n{}".format(live_all["live_room_id"])
								}
							]
						}
					},
					{
						"type": "action-group",
						"elements": [
							{
								"type": "button",
								"theme": "primary",
								"value": live_all["live_url"],
								"click": "link",
								"text": {
									"type": "plain-text",
									"content": "前往直播间"
								}
							}
						]
					}
				]
			}
		]
		card_view_json = (json.dumps(card_view, ensure_ascii=False))
		#print(live_all["live_type"])
		if live_all["live_type"] == "1":
			#print(UID_live_type)
			if UID_live_type == 1:
				print("主播昵称：" + live_all["name"])
				print("主播状态：直播中")
				print("检测到之前已经推送了\n跳过推送")
				return ("跳过推送")
			else: post_json = {
			"type":"10",
			"target_id":"5157605841527991",
			"content":card_view_json,
			}
			(requests.post(headers=bot_header,data=post_json,url="https://www.kaiheila.cn/api/v3/message/create").text)
		elif live_all["live_type"] == "0":
			print("主播昵称：" + live_all["name"])
			print("主播没有开播，不推送")
			print("主播状态：直播中")
			return 0
	else:print("error,找不到")
sql = "SELECT UID FROM BILIBILI_LIVE"
cursor.execute(sql)
UID_list = cursor.fetchall()
if __name__ == '__main__':
	while True:
		for UID in UID_list:
			print("-------------开始查询主播ID：" + str(UID[0]) + "-------------")
			time_num = random.randint(60,120)
			cardview_post(UID[0])
			time.sleep(10)
		print("数据库全库遍历完成，进入休眠，下次推送时间为:{}秒".format(time_num))
		time.sleep(time_num)

