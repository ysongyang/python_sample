import random,time
from class_mysql import *
from multiprocessing import Pool
import os, time

#多线程处理双色球生成
#处理球的号码，如果数字是1-9，则在前面加0，-> 09
def process_num(num):
    if num in range(1,10):
        num = str(num)
        new_num = '0' + num
    else:
        new_num = str(num)
    return  new_num

def generate_ball(count):
    red_ball = process_num(random.randint(1,34))
    blue_ball = process_num(random.randint(1,17))
    red_balls = [process_num(x) for x in range(1,34)] # 返回红球01-33的list
    blue_balls = [process_num(x) for x in range(1,17)] # 返回蓝球01-16的list
    ball_list = []
    for i in range(count):
        red_num = random.sample(red_balls, 6)  # 随机生成6位红球list
        red_num.sort()
        blue_num = random.sample(blue_balls, 1)[0]
        print(blue_num)
        cur_time = time.strftime('%Y-%m-%d %H:%M:%S')#当前时间格式化
        #ball = (' '.join(red_num),blue_num, cur_time)# 将红，蓝球，时间加入元祖
        data = {
            'red':' '.join(red_num),
            'blue':blue_num,
            'create_time':cur_time
        }
        add_ssq_data(data)
        #ball_list.append(ball) # 把每个结果加入list，[('25,18,23,28,24,19', '07', '2018-01-22 22:05:03'), ('16,23,27,07,31,21', '04', '2018-01-22 22:05:03')]
        #op_mysql(ball_list)
        #print(ball_list)


def add_ssq_data(data):
    ms = MYSQL()
    sql = "insert into lottery_ssq_data (`red`,`blue`,`create_time`) values ('%s' ,'%s' ,'%s')" % (
        data['red'], data['blue'], data['create_time'])
    #print(sql)
    #exit('===')
    return ms.ExecInsertQuery(sql)

if __name__ =='__main__':
    count = int(input('请输入你想生成的双色球号码数量：').strip())
    p = Pool()
    for i in range(4):
        p.apply_async(generate_ball, args=(count,))
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    #generate_ball(count)