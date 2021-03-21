#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 桜火, Inc. All Rights Reserved 
#
# @Time    : 2021/3/14 18:08
# @Author  : 桜火
# @Email   : xie@loli.fit
# @File    : listen.py
# @Software: PyCharm
import pymysql
from bilibili_dynamic.bilibili_dynamic.bilibili_test import get_dynamic_all_list
import json
uid = str(37958451)
cc = (get_dynamic_all_list(37958451))
pp = {}
for xx in cc:
	pp[xx]=1
ppp = str(json.dumps(pp))
db = pymysql.connect(host="127.0.0.1", user="test", password="TESTTEST", database="bilibili")
cursor = db.cursor()
# _sql = """INSERT INTO bilibili_dynamic(UID,NEW_dynamic_id)VALUES("""+"'"+UID + "'"+",'"+ppp+"')"
# print(_sql)
# cursor.execute(_sql)
# db.commit()
def find_sql_UID_dynamic(UID):

	sql = "SELECT * FROM bilibili_dynamic \
	       WHERE UID = %s" % (uid)
	cursor.execute(sql)
	results = cursor.fetchall()

	_result_dynamic=json.loads(results[0][2])
	return _result_dynamic
ccc = (find_sql_UID_dynamic(37958451))
for _dynamic_id in cc:
	print(_dynamic_id)
	print(ccc)
	if _dynamic_id in ccc:
		print("不包含")
		print(ccc)
	else:print("包含")


# for kjsdf in find_sql_UID_dynamic(37958451):
