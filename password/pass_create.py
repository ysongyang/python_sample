'''
def createPass():
    yield 1     #协程关键字 调用一次返回一次
    yield 2
    yield 3

T = createPass()

print(type(T))  #<class 'generator'>节约内存
print(next(T))
print(next(T))
print(next(T))
'''

import itertools

def createPass():
    for x in itertools.product("0123456789abcdefghijklmnopqrstuvwxyz",repeat=16):
        yield "".join(x)


crt_pass = createPass()

for i in range(1000):
    print(next(crt_pass))

while True:
    pass