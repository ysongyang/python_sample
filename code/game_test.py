#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/6 11:53
# @Author  : ysongyang
# @Site    : 
# @File    : game_test.py
# @Software: PyCharm

import random,sys,os


path=r"C:\Users\ysongyang\PycharmProjects\code\game.txt"
f = open(path)
lines = f.readlines()
f.close() # 关闭文件

scores = {} #初始化一个空字典
result = ""
for l in lines:
    s=l.split() #把每一行的数据拆分成list
    scores[s[0]] = s[1:] #第一项作为key，剩下的作为value

#scores  {'ysongyang': ['6', '1', '21']}

for n in scores:
    #把成绩按照“name game_times min_times total_times” 格式化
    #结尾要加上\n换行
    line = n+" "+" ".join(scores[n])+"\n"
    result += line #添加到result中