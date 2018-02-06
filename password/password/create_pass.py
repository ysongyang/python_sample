fpath = r"C:\Users\ysongyang\PycharmProjects\password\password\Countpassword.txt"
f = open(fpath,"rb")  #打开文件

myList = f.readlines() # 读取数据
print("加载数据完成")
f.close()
passList = []  #[32,111111] [31,123123]
for data in myList:
    data =data.decode("utf-8")
    tmpList = data.split(" ") #切割
    passList.append(tmpList)
print("写入次数列表完成")
del myList
# [32,111111]  x = 32
passList.sort(key=lambda x:int(x[0])) #按照次数排序 从小到大
passList.reverse() #反转 从大到小
print("排序完成")
wpath = r"C:\Users\ysongyang\PycharmProjects\password\password\Dictpassword.txt"
w = open(wpath,"wb")  #打开文件

for tmpList in passList:
    w.write((tmpList[0] + " " + tmpList[1]).encode("utf-8"))
print("写入数据完成")
del passList
w.close()