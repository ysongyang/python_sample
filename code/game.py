#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/6 11:21
# @Author  : ysongyang
# @Site    : 
# @File    : game.py
# @Software: PyCharm
from random import randint

name = input("请输入您的名字：")

path=r"C:\Users\ysongyang\PycharmProjects\code\game.txt"
f = open(path)
lines = f.readlines()
f.close() # 关闭文件

scores = {} #初始化一个空字典

for l in lines:
    s=l.split() #把每一行的数据拆分成list
    scores[s[0]] = s[1:] #第一项作为key，剩下的作为value

score = scores.get(name)  # 查找当前玩家的数据

if score is None: #如果没有找到
    score = [0, 0, 0] #初始化

game_times  = int(score[0])
min_times  = int(score[1])
total_times  = int(score[2])

if game_times > 0:

    avg_times = float(total_times) / game_times
else:
    avg_times = 0

#输出成绩信息，平均成绩保留2位小数
print("%s 你已经玩了%d次，最少%d轮猜出答案，平均%.2f轮猜出答案" % (name,game_times,min_times,avg_times))

num = randint(1,100)
times = 0 #记录本次游戏轮数
print("Guess what I think?")
bingo = False

while bingo==False:
    times +=1  #轮数+1
    answer = input()
    if answer.isdigit(): #判断是否为数字
        answer = int(answer)
    else:
        if answer == "exit":
          bingo = False
          break
        print("请输入数字")
        continue

    if answer < num:
        print("too smaill")
    if answer > num:
        print("too big!")
    if answer == num:
        print("bingo")
        bingo = True

if bingo == True:
    #如果是第一次玩，或者轮数比最小轮数少，则更新最小轮数
    if game_times ==0 or times < min_times:
        min_times = times

    total_times +=times #总游戏轮数增加
    game_times +=1 #游戏次数增加

    scores[name]=[str(game_times), str(min_times), str(total_times)]
    result = "" #初始化一个空的字符串用来存储数据

    # scores  {'ysongyang': ['6', '1', '21']}
    for n in scores:
        #把成绩按照“name game_times min_times total_times” 格式化
        #结尾要加上\n换行
        line = n+" "+" ".join(scores[n])+"\n"
        result += line #添加到result中

    #写入文件
    f = open(path,"w")
    f.write(result)
    f.close()
