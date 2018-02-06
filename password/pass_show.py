fpath = r"C:\Users\ysongyang\PycharmProjects\password\password\Dictpassword.txt"
f = open(fpath,"rb")  #打开文件

while True:
    line = f.readline() #能够读取不是空,不能读取no
    line = line.decode("utf-8") #解码
    password = line.split(" ") #切割
    print(password[1],end="")  #显示密码
    if not line:
        break

f.close()