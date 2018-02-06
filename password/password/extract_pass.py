
fpath = r"D:\BaiduNetdiskDownload\20180202尹成大神QQ77025077公开课\QQindex.txt"
f = open(fpath,"rb")  #打开文件

wpath = r"C:\Users\ysongyang\PycharmProjects\password\password\QQpassword.txt"
w = open(wpath,"wb")  #打开文件

dataList = f.readlines() #读取所有行到列表
for data in dataList:
    data = data.decode("utf-8","ignor") # 处理编码
    myList = data.split("----")
    print(myList[1],end="")
    w.write(myList[1].encode("utf-8"))

f.close() #关闭文件
w.close()