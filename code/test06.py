"""
f=open('data.txt')
data = f.readlines()
print(data)
f.close()


data = 'I will be in a file.\nSo cool!'
file = 'output.txt'
out = open(file,'w')
out.write(data)
out.close()

f = open('data.txt')
data = f.read()
out = open('data1.txt','w')
out.write(data)
out.close()
f.close()
"""

num = 1
data = ""
while num<6:
    print('第%d次请输入字符串：'% num)
    text = input()
    data = data + text + '\n'
    num +=1

print(data)
out = open('input.txt','w')
out.write(data)
out.close()