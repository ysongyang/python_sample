#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/6 12:20
# @Author  : ysongyang
# @Site    : 
# @File    : test09.py
# @Software: PyCharm
import urllib.request

web = urllib.request.urlopen("http://www.baidu.com")

content = web.read()

f = open("./baidu.html","wb")
f.write(content)
f.close()