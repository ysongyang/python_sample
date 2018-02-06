#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/6 16:39
# @Author  : ysongyang
# @Site    : 
# @File    : test10.py
# @Software: PyCharm
'''
class MyClass:
    name = 'Sam'
    def SayHi(self):
        print('Hello %s' % self.name)


mc = MyClass()
print(mc.name)
mc.name = 'lily'
mc.SayHi()
'''

#定义一个超类
class Vehicle:

    def __init__(self,speed):
        self.speed = speed

    def drive(self,distance):
        print('need %f hour(s)'% (distance/self.speed))

#定义一个汽车类 继承超类
class Car(Vehicle):
    def __init__(self,speed,fuel):
        Vehicle.__init__(self,speed)
        self.fuel = fuel

    def drive(self,distance):
        Vehicle.drive(self,distance)
        print('need %f fuels' % (distance*self.fuel))

#定义一个自行车类
class Bike(Vehicle):
    pass

bike = Bike(15.0)

car = Car(80.0,0.012)

bike.drive(100)
car.drive(100)
