#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/6 17:01
# @Author  : ysongyang
# @Site    : 
# @File    : test12.py
# @Software: PyCharm


#lst_1 = [1,2,3,4,5,6]

def double_func(x):

    return x * 2

#lst_2 = map(double_func, lst_1)

lst_1 = (1,2,3,4,5,6)
lst_2 = map(lambda x: x * 2, lst_1)
print(lst_2)