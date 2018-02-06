#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/6 14:51
# @Author  : ysongyang
# @Site    : 读取xml文件案例
# @File    : city_get.py
# @Software: PyCharm
from xml.etree.ElementTree import parse

file ="./city.xml"
doc = parse(file)
#获取跟节点
root = doc.getroot()
result = "city={\n"
# 获取根节点下面的下一节点
for provinces in root.findall('province'):
    for citys in provinces.findall('city'):
        for countys in citys.findall('county'):
            #{'id': '010101', 'name': '北京', 'weatherCode': '101010100'}
            data = countys.attrib
            line = "  '%s': '%s',\n" % (data['name'],data['weatherCode'])
            result +=line
            #print(data['name']+':'+data['weatherCode'])
result +="}"
f = open("./city.py",'w',encoding="utf8") #新建一个文件city.py 编码格式为utf-8
f.write(result)
f.close()