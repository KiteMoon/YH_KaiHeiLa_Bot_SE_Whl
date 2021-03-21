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
db = pymysql.connect(host="127.0.0.1", user="test", password="TESTTEST", database="kaiheila")
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
		print("他没直播了")
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
	_sql_find = "SELECT LIVE_TYPE FROM bilibili_live WHERE UID={}".format(UID)
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
				print("检测到之前已经推送了，跳过推送")
				return ("跳过推送")
			else: post_json = {
			"type":"10",
			"target_id":"5157605841527991",
			"content":card_view_json,
			}
			(requests.post(headers=bot_header,data=post_json,url="https://www.kaiheila.cn/api/v3/message/create").text)
	else:print("error,找不到")
sql = "SELECT UID FROM bilibili_live"
cursor.execute(sql)
UID_list = cursor.fetchall()
if __name__ == '__main__':
	for UID in UID_list:
		cardview_post(UID[0])
