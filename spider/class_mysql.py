#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/6 18:18
# @Author  : ysongyang
# @Site    : mysql 连接类
# @File    : class_mysql.py
# @Software: PyCharm
import pymysql  #pip install pymysql

class MYSQL():
    def __init__(self,host='localhost',port=3306,user='root',pwd='root',db='spider'):
        self.host = host
        self.port = port
        self.user = user
        self.pwd = pwd
        self.db = db

    #得到连接信息，返回conn.cursor
    def __GetConnect(self):
        if not self.db:
            print("没有设置数据库信息")
            return
        try:
            self.conn = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                passwd=self.pwd,
                db=self.db,
                charset='utf8'
            )
        except Exception as e:
            print("数据库链接失败",e)
            return

        return self.conn.cursor()

    #执行查询语句，返回的是一个包含tuple的list，list的元素是记录行，tuple的元素是记录行的字段
    def ExecQuery(self,sql):
        cur = self.__GetConnect()
        if cur is None:
            return
        cur.execute(sql)
        resList = cur.fetchall()
        #查询完毕后必须关闭连接
        self.conn.close()
        if len(resList)==0:
            return None
        return resList

    # 执行查询语句，返回行数
    def ExecQueryCount(self, sql):
        cur = self.__GetConnect()
        if cur is None:
            return
        cur.execute(sql)
        resCount = cur.rowcount
        # 查询完毕后必须关闭连接
        self.conn.close()
        return resCount

    #执行非查询语句
    def ExecNonQuery(self,sql):
        cur = self.__GetConnect()
        if cur is None:
            return
        try:
            cur.execute(sql)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(e)
        # 查询完毕后必须关闭连接
        self.conn.close()

    #执行插入语句
    def ExecInsertQuery(self,sql):
        lastid = 0
        cur = self.__GetConnect()
        if cur is None:
            return
        try:
            cur.execute(sql)
            self.conn.commit()
            lastid = cur.lastrowid
        except Exception as e:
            self.conn.rollback()
            print(e)
        # 查询完毕后必须关闭连接
        self.conn.close()
        return lastid