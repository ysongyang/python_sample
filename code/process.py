#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/6 15:04
# @Author  : ysongyang
# @Site    : 进程池示例
# @File    : process.py
# @Software: PyCharm

from multiprocessing import Pool
import os,time,random


def worker(msg):
    startTime = time.time() #返回时间戳
    print("%s 开始执行,进程号为 %d" % (msg,os.getpid()))
    time.sleep(random.random()*2)
    endTime = time.time()
    print(msg,"执行完毕，耗时%0.2f" % (endTime-startTime))

if __name__ == '__main__':

    pool = Pool(3) #实例化3个进程

    for i in range(0,10):
        #pool.apply(worker,(i,)) #是阻塞的
        pool.apply_async(worker,(i,))  #非阻塞
    print("start... ...")
    pool.close()
    pool.join()
    print("end... ...")