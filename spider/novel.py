#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/7 16:55
# @Author  : ysongyang
# @Site    : 采集全书网内容列表
# @File    : novel.py
# @Software: PyCharm

import requests
import queue
import threading
import urllib.request
import re, os, time
from class_mysql import *
from datetime import datetime
from bs4 import BeautifulSoup


class Crawl_thread(threading.Thread):
    '''
    抓取线程类
    '''

    def __init__(self, thread_id, queue):
        threading.Thread.__init__(self)
        self.thread_id = thread_id  # 线程ID
        self.queue = queue  # 队列

    def run(self):
        print(u'启动了线程,{}'.format(self.thread_id))  # 加u 表示 unicode编码
        self.crawl_spider()
        print(u'退出了线程,{}'.format(self.thread_id))

    def crawl_spider(self):
        while True:
            if self.queue.empty():  # 判断队列是否为空
                break
            else:
                '''
                item = {
                    'page': page,
                    'url': cateUrl,
                    'sort_id': sort_id,
                    'sort_name': sort_name
                }
                '''
                item = self.queue.get()  # 获取队列里的元素    出队
                url = item['url']
                # print(u'当前正在工作线程是【{}】,正在采集第 {} 页，URL地址是 {}'.format(self.thread_id, str(item['page']), str(url)))
                # url = 'https://www.qiushibaike.com/8hr/page/{}/'.format(page)
                try:
                    # req = urllib.request.Request(url, headers=headers)
                    # html = urllib.request.urlopen(req).read().decode('gbk')  # 转码   .encode('utf-8').decode('utf-8')
                    # content = requests.get(self.url,headers=headers)
                    datas = {
                        'url': url,
                        'sort_id': item['sort_id'],
                        'sort_name': item['sort_name']
                    }
                    data_quere.put(datas)  # 将数据入队做数据抓取处理
                    #time.sleep(2)
                    # print(html)
                except Exception as e:
                    print(u'采集线程错误', e)


class Parser_thread(threading.Thread):
    '''
    解析网页的类
    '''

    def __init__(self, thread_id, queue):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.queue = queue

    def run(self):
        print(u'启动了解析线程,{}'.format(self.thread_id))  # 加u 表示 unicode编码

        while False == flag:
            try:
                # get的参数为false的时候，队列为空 抛出异常
                item = self.queue.get()
                if not item:
                    pass
                self.parse_data(item)
                self.queue.task_done()  # 每当get一次后，告诉队列该任务已经处理完毕。
            except Exception as e:
                print('解析线程出错', e)
                pass
        print(u'退出了解析线程,{}'.format(self.thread_id))  # 加u 表示 unicode编码

    def parse_data(self, item):
        '''
        解析每个栏目的网页内容的函数
        :param item:
        :return:
        '''
        try:
            res = requests.get(item['url'], timeout=5, headers=headers)
            if res.status_code == 404:
                pass
            res.encoding = 'gbk'
            soup = BeautifulSoup(res.text, 'html.parser')
            urlList = soup.select('section ul.seeWell > li > a')
            numList = len(urlList)  # 32条数据
            for url in urlList:
                url = url.get('href')
                #print("当前栏目页 %s ，采集的url %s " % (item['url'], url))
                book_str = url.split('_')
                book_str = str(book_str[1]).split('.')
                if len(book_str) > 0:
                    book_id = book_str[0]
                    if isNovelBookId(book_id) is None:
                        getNovel(url, item['sort_id'], item['sort_name'], book_id)
                        print('book_id %d 已入库！' % int(book_id))
                    else:
                        print('book_id %d 已存在！' % int(book_id))
                else:
                    pass
                #time.sleep(2)  # 2秒执行一次
        except Exception as e:
            print('解析出错', e)
            pass


data_quere = queue.Queue()  # 创建一个队列


flag = False  # 全局变量

# 定义一个字典对应栏目名称
sort_dict = {
    1: '玄幻魔法',
    2: '武侠修真',
    3: '纯爱耽美',
    4: '都市言情',
    5: '职场校园',
    6: '穿越重生',
    7: '历史军事',
    8: '网游动漫',
    9: '恐怖灵异',
    10: '科幻小说',
    11: '美文名著',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'}

"""
url         小说url
sort_id     栏目id
sort_name   栏目名称
book_id     小说id，标识符
"""
# 获取小说内容
def getNovel(url, sort_id, sort_name, book_id):
    req = urllib.request.Request(url, headers=headers)
    html = urllib.request.urlopen(req).read().decode('gbk')  # 转码   .encode('utf-8').decode('utf-8')
    # 获取小说书名
    reg = r'<meta property="og:novel:book_name" content="(.*?)"/>'
    book_name = re.findall(reg, html)[0]
    # 获取小说描述
    reg = r'<meta property="og:description" content="(.*?)"/>'
    description = re.findall(reg, html, re.S)[0]
    description = description.replace("&nbsp;", "")
    # 获取小说封面图
    reg = r'<meta property="og:image" content="(.*?)"/>'
    image = re.findall(reg, html)[0]
    # 获取作者
    reg = r'<meta property="og:novel:author" content="(.*?)"/>'
    author = re.findall(reg, html)[0]
    # 获取状态
    reg = r'<meta property="og:novel:status" content="(.*?)"/>'
    status = re.findall(reg, html)[0]

    # 获取更新时间
    reg = r'<meta property="og:novel:update_time" content="(.*?)"/>'
    update_time = re.findall(reg, html)[0]
    # 获取章节开始阅读的URL
    reg = r'<a href="(.*?)" class="reader" '
    chapterUrl = re.findall(reg, html)[0]

    # print(book_name,description,image,author,status,update_time,chapterUrl)
    data = {
        'sort': sort_id,
        'sortname': sort_name,
        'name': book_name,
        'image': image,
        'description': description.replace('<br />\n', ''),
        'status': status,
        'author': author,
        'book_id': book_id,
        'book_url': url,
        'chatper_url': chapterUrl,
        'create_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'update_time': update_time
    }
    # print(data)
    lastrwoid = addNovelData(data)  # 新增小说返回新增的主键id
    return lastrwoid


def isNovelBookId(book_id):
    ms = MYSQL()
    sql = "select * from novel where book_id = %d " % int(book_id)
    info = ms.ExecQuery(sql)
    return info


# 插入小说数据
def addNovelData(data):
    ms = MYSQL()
    sql = "insert into novel(`sort`,`sortname`,`name`,`image`,`description`,`status`,`author`,`book_id`,`book_url`,`chatper_url`,`create_time`,`update_time`) values (%d , '%s' , '%s' , '%s' , '%s' , '%s' , '%s' , '%s' , '%s', '%s' , '%s' , '%s' )" % (
        int(data['sort']), data['sortname'], data['name'], data['image'], data['description'], data['status'],
        data['author'], data['book_id'], data['book_url'], data['chatper_url'], data['create_time'],
        data['update_time'])
    # print(sql)
    lastrwoid = ms.ExecInsertQuery(sql)
    del sql
    return lastrwoid


def main(sort_id, start_page, end_page):

    # 循环栏目字典
    # for sort_id, sort_name in sort_dict.items():  # sort_dict是一个字典，所以需要使用 .items()
    url = "http://www.quanshuwang.com/list/%d_1.html" % (sort_id)

    '''
    #urllib写法
    req = urllib.request.Request(url, headers=headers)
    html = urllib.request.urlopen(req).read().decode('gbk')  # 转码   .encode('utf-8').decode('utf-8')
    reg = r'<em id="pagestats">(.*?)</em>'  # 获取总页码数
    page_text = re.findall(reg, html)
    max_page 
    '''
    # soup写法
    # res = requests.get(url, timeout=5, headers=headers)
    # res.encoding = 'gbk'
    # soup = BeautifulSoup(res.text, 'html.parser')
    # page_text = soup.select('.pagelink > em')[0].text
    # max_page = page_text.split('/')[1]
    max_page = 20
    if end_page - start_page > max_page:
        print('每次最多采集%d页' % max_page)
    pageQueue = queue.Queue(50)  # 初始化队列
    for page in range(start_page, end_page):  # 100任务
        cateUrl = "http://www.quanshuwang.com/list/%d_%d.html" % (sort_id, page)
        # print(cateUrl)
        item = {
            'page': page,
            'url': cateUrl,  # 栏目url
            'sort_id': sort_id,
            'sort_name': sort_dict[sort_id]
        }
        pageQueue.put(item)  # 放入队列

    # 初始化采集线程
    crawl_threads = []
    crawl_name_list = ['采集线程1', '采集线程2', '采集线程3', '采集线程4', '采集线程5']  # 几个线程同时工作
    for thread_id in crawl_name_list:
        thread = Crawl_thread(thread_id, pageQueue)
        thread.start()
        crawl_threads.append(thread)

    # 初始化解析线程
    parser_threads = []
    parser_name_list = ['解析线程1', '解析线程2', '解析线程3', '解析线程4', '解析线程5']
    for thread_id in parser_name_list:
        thread = Parser_thread(thread_id, data_quere)
        thread.start()
        parser_threads.append(thread)

    # 等待队列清空
    while not pageQueue.empty():  # 采集队列
        pass

    # 等待所有的采集线程结束
    for t in crawl_threads:
        t.join()  # 阻塞调用线程，直到队列中的所有任务被处理掉

    while not data_quere.empty():  # 解析队列
        pass

    # 通知线程退出
    global flag
    flag = True

    # 等待所有的解析线程结束
    for t in parser_threads:
        t.join()  # 阻塞调用线程，直到队列中的所有任务被处理掉

    print(u"退出主线程")
    # output.close()


if __name__ == '__main__':
    main(1, 19, 50)
