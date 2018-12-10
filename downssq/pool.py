#! /usr/bin/env python
# -*- coding:utf-8   -*-
# __author__ == "tyomcat"
# "我的电脑有4个cpu"

from multiprocessing import Pool
import os, time

def long_time_task(name):
    print ('Run task %s (%s)...' % (name, os.getpid()))
    start = time.time()
    time.sleep(3)
    end = time.time()
    print ('Task %s runs %0.2f seconds.' % (name, (end - start)))

if __name__=='__main__':
    count = int(input('请输入你想生成的双色球号码数量：').strip())
    print ('Parent process %s.' % os.getpid())
    p = Pool()
    for i in range(4):
        p.apply_async(long_time_task, args=(count,))
    print ('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print ('All subprocesses done.')