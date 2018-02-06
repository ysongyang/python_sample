fpath = r"C:\Users\ysongyang\PycharmProjects\password\password\QQpassword.txt"
f = open(fpath,"rb")  #打开文件

wpath = r"C:\Users\ysongyang\PycharmProjects\password\password\Sortpassword.txt"
w = open(wpath,"wb")  #打开文件

passList = f.readlines()
print("读取完成")
passList.sort()
print("排序完成")

for password in passList:

    w.write(password)

print("写入完成")
f.close()
w.close()