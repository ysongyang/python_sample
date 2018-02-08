#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/8 15:57
# @Author  : ysongyang
# @Site    : 爬淘宝搜索内容的示例
# @File    : taobao_search.py
# @Software: PyCharm
import time
import requests
import json
from fiter_tags import *
import xlwt

t = time.localtime()
datas = []
data_s = []
tags = FiterTags()
flag = True

def CrawlerData(find_word, page):
    # 参数
    find_args = {
        'q': find_word,  # 搜索的关键字
        'initiative_id': 'staobaoz_%s%02d%02d' % (t[0], t[1], t[2]),  # 页码
        'sort': 'sale-desc',  # 销量排序
    }

    search_url = "https://s.taobao.com/search?imgfile=&js=1&stats_click=search_radio_all%3A1&ie=utf8&cd=false"

    # 发送请求
    r = requests.get(search_url, params=find_args)
    if r.status_code == 404:
        pass
    # print(r.url)
    html = r.text
    cookie_ = r.cookies  # 取cookies
    # 分析找出信息
    reg = r"g_page_config = (.*?)g_srp_loadCss"  # 定义正则匹配出我们需要的内容
    content = re.findall(reg, html, re.S)[0].replace(";", "")
    content = json.loads(content)
    data_list = content['mods']['itemlist']['data']['auctions']
    # 处理数据
    datasAdd(data_list)

    # 爬取剩下的页数
    for i in range(1, int(page)):
        ktsts = time.time()
        find_args['_ksTS'] = "%s_%s" % (int(ktsts * 1000), str(ktsts))[-3:]
        find_args['callback'] = "jsonp%d" % (int(str(ktsts)[-3:]) + 1)
        find_args['data-value'] = 44 * i
        url = "https://s.taobao.com/search?data-key=s&data-value=44&ajax=true&_ksTS=1518081032712_1061&callback=jsonp1062&q=%E7%94%B5%E8%A7%86&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20180208&ie=utf8&cd=false&sort=sale-desc&bcoffset=0&p4ppushleft=%2C44".format(
            time.time())
        if i > 1:
            find_args['s'] = 44 * (i - 1)

        req = requests.get(url, params=find_args, cookies=cookie_)
        if req.status_code == 404:
            pass
        html = req.text  # 返回的是json数据格式
        content = re.findall(r"{.*}", html, re.S)[0]
        content = json.loads(content)
        data_list = content['mods']['itemlist']['data']['auctions']
        #数据写入
        data_s = datasAdd(data_list)
        cookie_ = req.cookies #更新cookies
    #数据处理写入文件
    WriteXls(data_s, find_word)


def datasAdd(data_list):
    for item in data_list:
        temp = {
            'title': tags.filter_tags(item['title']),
            'pic_url': 'https:' + item['pic_url'],
            'view_price': item['view_price'],  # 销售价
            'view_sales': item['view_sales'],  # 多少人付款
            'view_fee': '否' if float(item['view_fee']) else '是',  # 运费
            'isTmail': '是' if item['shopcard']['isTmall'] else '否',  # 是否天猫
            'area': item['item_loc'],
            'name': item['nick'],
            'detail_url': item['detail_url'],

        }
        datas.append(temp)
    return datas


'''
将数据写入到xls文件中
'''


def WriteXls(datas, find_word):
    # 持久化
    file = xlwt.Workbook(encoding='utf-8')
    sheet01 = file.add_sheet(u'sheet1', cell_overwrite_ok=True)

    # 写标题
    sheet01.write(0, 0, '标题')
    sheet01.write(0, 1, '图片')
    sheet01.write(0, 2, '标价')
    sheet01.write(0, 3, '购买人数')
    sheet01.write(0, 4, '是否包邮')
    sheet01.write(0, 5, '是否天猫')
    sheet01.write(0, 6, '地区')
    sheet01.write(0, 7, '店名')
    sheet01.write(0, 8, '详情url')
    # 循环写入数据
    for i in range(len(datas)):
        sheet01.write(i + 1, 0, datas[i]['title'])
        sheet01.write(i + 1, 1, datas[i]['pic_url'])
        sheet01.write(i + 1, 2, datas[i]['view_price'])
        sheet01.write(i + 1, 3, datas[i]['view_sales'])
        sheet01.write(i + 1, 4, datas[i]['view_fee'])
        sheet01.write(i + 1, 5, datas[i]['isTmail'])
        sheet01.write(i + 1, 6, datas[i]['area'])
        sheet01.write(i + 1, 7, datas[i]['name'])
        sheet01.write(i + 1, 8, datas[i]['detail_url'])

    file.save(u'爬取%s的结果.xls' % find_word)
    print(u'爬取数据成功')



if __name__ == '__main__':

    print("请输入你要爬的关键词（内容）信息")
    find_word = input()
    print("请输入要爬的页数")
    page = input()
    if page.isdigit():  # 判断是否为数字
        page = int(page)
        CrawlerData(find_word, page)
    else:
        print("输入的页数有误")



