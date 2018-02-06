#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/6 16:51
# @Author  : ysongyang
# @Site    : 
# @File    : test11.py
# @Software: PyCharm

import re

text = "Hi, I am Shirley Hilton. I am his wife."

m = re.findall(r"I.*e",text)
print(m)

text = "site sea sue sweet see case sse ssee loses"

print(re.findall(r"\bs\S*e\b",text)) # \b  称为单词边界（word boundary）符