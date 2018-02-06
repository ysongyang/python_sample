import itertools #导入生成密码库

#迭代器 生成器 repeat=6 可以重复6次
passlist = ["".join(x) for x in itertools.product("0123456789",repeat=6)]

for password in passlist:
    print(password)

while True: #死循环卡住
    pass


#纯数字密码8位 需要6G内存 ， 9位 60G内存 ， 11位  6000G内存