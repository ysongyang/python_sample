#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/7 16:55
# @Author  : ysongyang
# @Site    : 采集小说下的章节（多线程）
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


data_quere = queue.Queue()  # 创建一个队列
flag = False  # 全局变量
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'}


'''
抓取线程类
'''
class Crawl_thread(threading.Thread):

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

                item = self.queue.get()  # 获取队列里的元素    出队
                print(item)
                # print(u'当前正在工作线程是【{}】,正在采集第 {} 页，URL地址是 {}'.format(self.thread_id, str(item['page']), str(url)))
                # url = 'https://www.qiushibaike.com/8hr/page/{}/'.format(page)
                try:
                    datas = {
                        'url': item['url'],
                        'navel_id': item['navel_id'],
                    }
                    data_quere.put(datas)  # 将数据入队做数据抓取处理
                    # time.sleep(2)
                    # print(html)
                except Exception as e:
                    print(u'采集线程错误', e)
'''
解析网页的类
'''
class Parser_thread(threading.Thread):

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
            print(item)
            res = requests.get(item['url'], timeout=15, headers=headers)
            if res.status_code == 404:
                pass
            res.encoding = 'gbk'
            soup = BeautifulSoup(res.text, 'html.parser')
            chapter_title = soup.select('.chapName > strong')[0].text
            urlList = soup.select('.chapterNum ul .dirconone > li > a')
            numList = len(urlList)  # 章节的数据
            '''
            根据章节的数据量 判断数据库的数据是否相等，不等则进行数据入库处理，相等则跳过处理
            '''
            dataNum = queryChapterCount(item['navel_id'])
            if int(numList) == int(dataNum):
                pass
            else:
                for chapter_url in urlList:
                    # print(item['url'], chapter_url.get('href'), chapter_title, item['navel_id'])
                    getChapterContent(item['url'], chapter_url.get('href'), chapter_url.text, item['navel_id'])
                    # time.sleep(2)  # 2秒执行一次
        except Exception as e:
            print('解析出错', e)
            pass


# 获取章节内容
"""
url             小说url
chapter_url     小说章节url
chapter_title   小说章节标题
lastrowid       novel表主键id
"""


def getChapterContent(url, chapter_url, chapter_title, lastrowid):
    try:
        res = requests.get(chapter_url, timeout=15, headers=headers)
        if res.status_code == 404:
            pass
        res.encoding = 'gbk'
        soup = BeautifulSoup(res.text, 'html.parser')
        # title = soup.select('.jieqi_title')[0].text.lstrip('章 节目录 ')
        content = soup.select('#content')[0].text.lstrip('style5();').rstrip('style6();')
        chapter_id = chapter_url.split('/')[-1].split('.')[0]

        if isNovelChapterId(chapter_id) is None:
            data = {
                'novel_id': lastrowid,
                'title': chapter_title,
                'content': content,
                'chapter_id': chapter_id,
                # http://www.quanshuwang.com/book/144/144052/39966954.html
                'book_url': url,  # 小说的url
                'chapter_url': chapter_url,  # 章节的url
                'create_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            }
            # 插入章节内容
            # print(chapter_title)
            addChapterData(data)
            print('chapter_id %d 已入库！' % int(chapter_id))
        else:
            print('chapter_id %d ****已存在！****' % int(chapter_id))


    except Exception as e:
        print('采集章节内容出错', e)
        pass


# 判断章节是否存在
def isNovelChapterId(chapter_id):
    ms = MYSQL()
    sql = "select * from chapter where chapter_id = %d " % int(chapter_id)
    info = ms.ExecQuery(sql)
    return info


# 插入章节数据
def addChapterData(data):
    ms = MYSQL()
    chapter_id = data['chapter_id']
    # 如果数据不存在则进行插入数据
    if isNovelChapterId(chapter_id) is None:
        sql = "insert into chapter (`novel_id`,`title`,`content`,`chapter_id`,`book_url`,`chapter_url`,`create_time`) values (%d ,'%s' ,'%s' ,'%s','%s','%s','%s')" % (
            data['novel_id'], data['title'], data['content'], data['chapter_id'], data['book_url'], data['chapter_url'],
            data['create_time'])
        # print(sql)
        ms.ExecInsertQuery(sql)
    else:
        pass

'''
每次处理5条数据
并记录本次采集的页码  每次加载5页
:return:
'''
def queryNovel(page=0):
    ms = MYSQL()
    sql = "SELECT `id`,`book_id`,`chatper_url` from novel WHERE `status` like '%%%s%%' ORDER BY id asc LIMIT %d,5" % (
        str('连载'), int(page))
    info = ms.ExecQuery(sql)
    return info


'''
根据小说表主键ID查询采集的章节条目
'''
def queryChapterCount(novel_id):
    ms = MYSQL()
    sql = "select * from chapter where novel_id = %d " % int(novel_id)
    return ms.ExecQueryCount(sql)

'''
主函数定义
'''
def main():
    pageFile = 'page.txt'
    if os.path.exists(pageFile):
        f = open(pageFile)
        page = f.read()
        f.close()
    else:
        w = open(pageFile, 'w')
        w.write('0')
        w.close()
    infos = queryNovel(int(page))
    data_len = len(infos)
    pageQueue = queue.Queue(int(data_len) + 1)  # 初始化队列
    for info in infos:
        item = {
            'navel_id': info[0],
            'url': info[-1]
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
    # 如果没有数据则退出程序
    if infos is None:
        os._exit(0)
    else:

        '''
        将当前页存入file文件
        因为每次page每页显示5条数据，所以这里主线程退出后加5复调继续执行函数
        '''
        page = int(page) + 5
        w = open(pageFile, 'w')
        w.write(str(page))
        w.close()
        flag = False  # 通知线程开始
        main()
    # output.close()


if __name__ == '__main__':
    main()
