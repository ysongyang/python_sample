'''
mylist =[1111,1111,2222,2222,3333,4444,4444,5555,5555,6666]
length = len(mylist)
i = 0
while i<length:
    count = 1 #密码次数
    password = mylist[i]
    while i+1 <= length-1 and mylist[i] == mylist[i+1]:
        count+=1
        i+=1
    print(count,password)
    i+=1
'''

fpath = r"C:\Users\ysongyang\PycharmProjects\password\password\Sortpassword.txt"
f = open(fpath,"rb")  #打开文件

wpath = r"C:\Users\ysongyang\PycharmProjects\password\password\Countpassword.txt"
w = open(wpath,"wb")  #打开文件

myList = f.readlines()
length = len(myList)
i=0
while i<length:
    count = 1 #次数
    password = myList[i].decode("UTF-8","ignor") #密码
    while i + 1 <= length - 1 and myList[i] == myList[i + 1]:
        count += 1
        i += 1
    #print(count, password)
    i += 1
    w.write((str(count)+" "+password).encode('UTF-8'))

f.close()
w.close()