#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/6 15:50
# @Author  : ysongyang
# @Site    : 
# @File    : process_test01.py
# @Software: PyCharm

import multiprocessing
import os,time,random


def Lee():
    print("\nRun task Lee-%s" % (os.getpid()))  # os.getpid()获取当前的进程的ID
    start = time.time()
    time.sleep(random.random() * 10)  # random.random()随机生成0-1之间的小数
    end = time.time()
    print('Task Lee, runs %0.2f seconds.' % (end - start))


def Marlon():
    print("\nRun task Marlon-%s" % (os.getpid()))
    start = time.time()
    time.sleep(random.random() * 40)
    end = time.time()
    print('Task Marlon runs %0.2f seconds.' % (end - start))


def Allen():
    print("\nRun task Allen-%s" % (os.getpid()))
    start = time.time()
    time.sleep(random.random() * 30)
    end = time.time()
    print('Task Allen runs %0.2f seconds.' % (end - start))


def Frank():
    print("\nRun task Frank-%s" % (os.getpid()))
    start = time.time()
    time.sleep(random.random() * 20)
    end = time.time()
    print('Task Frank runs %0.2f seconds.' % (end - start))

if __name__ == "__main__":

    fun_list = [Lee,Marlon,Allen,Frank]
    pool = multiprocessing.Pool(4)
    for fun in fun_list:
        pool.apply_async(fun)

    print('Waiting for all subprocesses done...')
    pool.close()
    pool.join()  # 调用join之前，一定要先调用close() 函数，否则会出错, close()执行后不会有新的进程加入到pool,join函数等待素有子进程结束
    print('All subprocesses done.')