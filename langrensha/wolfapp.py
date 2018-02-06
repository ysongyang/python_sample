# !/usr/bin/env python
# *coding:utf-8*
from hashlib import sha1
from tornado import web,ioloop,httpserver
import os
import time
import random

# 用户信息
USER_INFO = {}
# 可用房间
ROOMS = {'%d' % key:{} for key in range(1,1001)}
# 已用房间
USING_ROMMS = {}
# 牌,游戏配置
PLAYER_SETTING={
    8:{'狼人':3,'预言家':1,'女巫':1,'猎人':1,'平民':2},
    9:{'狼人':3,'预言家':1,'女巫':1,'猎人':1,'平民':3},
    10:{'狼人':4,'预言家':1,'女巫':1,'猎人':1,'平民':3},
    11:{'狼人':4,'预言家':1,'女巫':1,'猎人':1,'平民':4},
    12:{'狼人':4,'预言家':1,'女巫':1,'猎人':1,'平民':5},
}
# 逻辑处理模块 部门
# 首页
class IndexHandler(web.RequestHandler):
    def get(self,*args,**kwargs):

        #检查cookie
        person_id = self.get_cookie('person_id')
        if not person_id:
            #第一次来 给一个身份
            person_id = sha1(("%s%s" % (os.urandom(16), time.time())).encode('utf-8')).hexdigest()
            #设置到cookie
            self.set_cookie('person_id',person_id)
        #将用户添加到USER_INFO
        if person_id not in USER_INFO:
            USER_INFO[person_id]={
                'time':time.time(),#记录登录时间
                'name':''
            }
        self.render('index.html')

class CreateGameHandler(web.RequestHandler):

    def post(self, *args, **kwargs):
        # 判断有没有去前台登记
        person_id = self.get_cookie('person_id')
        if not person_id or person_id not in USER_INFO:
            self.render('error.html',info={
                'status':False,
                'info':'超时刷新',
                'second': 3,
                'url':'/'
            })
            return
        # 判断是否还有房间
        # 创建房间
        try:
            room_num,room_info = ROOMS.popitem()
        except Exception as e:
            print(e)
            self.render('error.html', info={
                'status': False,
                'info': '房间已满,稍后在访问',
                'second': 3,
                'url': '/'
            })
            return
        # 检查 收入的num
        try:
            player_num = int(self.get_argument('player_num'))
            # 获取游戏配置
            player_setting = PLAYER_SETTING[player_num]
        except Exception as e:
            print(e)
            self.render('error.html', info={
                'status': False,
                'info': '请输入正确的人数',
                'second': 3,
                'url': '/'
            })
            return
        # 生成房间信息
        room_info['time'] = time.time()
        room_info['num'] = room_num
        room_info['judge'] = person_id
        room_info['player_list'] = []
        # 生成座位
        for key in player_setting:
            for i in range(player_setting[key]):
                room_info['player_list'].append(
                    {'role':key,'player':'还没有加入','person_id':''}
                )
        # 打乱顺序
        random.shuffle(room_info['player_list'])
        # 更新房间信息
        USING_ROMMS[room_num] = room_info

        # 更新用户信息
        USER_INFO[person_id]['room_num'] = room_num
        USER_INFO[person_id]['role'] = 'judge'

        # 更新时间
        USER_INFO[person_id]['time'] = room_info['time']

        print(USER_INFO)
        # 进入房间
        self.render('game.html',room_num=room_num,
                    player_list = room_info['player_list'],
                    settings = player_setting)

    def get(self, *args, **kwargs):
        room_num = int(self.get_argument('room_num'))
        print(room_num)
        print(USER_INFO)
        print(USING_ROMMS)



class JoinGameHandler(web.RequestHandler):
    def post(self, *args, **kwargs):
        pass


#设置
settings = {
    #模板设置
    'template_path':'template',
    'static_path':'static',
    'static_url_prefix':'/static/'
}

#路由系统 分机号
application = web.Application([
    (r"/",IndexHandler),
    (r"/create_game",CreateGameHandler),
    (r"/join_game",JoinGameHandler),
    ],**settings)

if __name__ =='__main__':
    # socket服务器
    http_server = httpserver.HTTPServer(application)
    http_server.listen(8080)
    ioloop.IOLoop.current().start()
