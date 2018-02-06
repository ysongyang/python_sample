import zipfile # 导入zip包

def checkPass(password): # 破解密码函数
    spath=r"C:\Users\ysongyang\PycharmProjects\password\jiami\password.zip"
    password=password[:-2]
    password = password.encode("UTF-8")

    try:
        myzipFile = zipfile.ZipFile(spath)
        myzipFile.extractall(path=r"C:\Users\ysongyang\PycharmProjects\password\jiami",pwd=password)
        print("密码正确",password)
        return True
    except:
        print("密码错误",password)
        return False

fpath = r"C:\Users\ysongyang\PycharmProjects\password\password\Dictpassword.txt"
f = open(fpath,"rb")  #打开文件

while True:
    line = f.readline() #能够读取不是空,不能读取no
    line = line.decode("utf-8") #解码
    password = line.split(" ") #切割
    isok = checkPass(password[1])
    if isok:
        print("===================找到密码")
        break
    #print(password[1],end="")  #显示密码
    else:
        print("===================密码错误")

    if not line:
        break

f.close()