#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/6 12:25
# @Author  : ysongyang
# @Site    : 
# @File    : weather.py
# @Software: PyCharm
from city import city
import urllib.request
import json
import time

def funCity(cityCode):
    if cityCode:
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',
            'Host': 'd1.weather.com.cn',
            'Referer': 'http://www.weather.com.cn/weather1dn/%.shtml' % cityCode,
        }
        try:
            url = ("http://d1.weather.com.cn/sk_2d/%s.html" % cityCode)
            url_s = ("http://d1.weather.com.cn/dingzhi/%s.html" % cityCode)
            time.sleep(3) #延迟3秒
            req = urllib.request.Request(url=url,headers=header)
            req_s = urllib.request.Request(url=url_s,headers=header)

            content= urllib.request.urlopen(req).read().decode('utf-8')
            content_s= urllib.request.urlopen(req_s).read().decode('utf-8')
            str_split = content.split("=")
            str_split_s = content_s.split(";")
            str_split_s_ = str_split_s[0].split("=")

            data = json.loads(str_split[1])
            data_s = json.loads(str_split_s_[1])
            data_s = data_s['weatherinfo']
            #print(data)
            #print(data_s)
            str_temp = ("数据最新时间：%s \n"
                        "当前温度：%s\n"
                        "今天天气：%s\n"
                        "最高温度：%s 最低温度：%s\n"
                        "空气指数：%s\n"
                        % (data['time'],
                           data['temp'],
                           data['weather'],
                           data_s['temp'],
                           data_s['tempn'],
                           data['aqi']))
            print(str_temp)
        except:
            print("查询失败")
    else:
        print("没有找到该城市")

if __name__ == '__main__':

    cityName = input("你想查那个城市的天气?\n")
    cityCode = city.get(cityName)
    funCity(cityCode)