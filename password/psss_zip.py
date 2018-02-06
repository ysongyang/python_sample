import zipfile

"""
spath="C:\\Users\\ysongyang\\PycharmProjects\\password"
#压缩文件
zipfile=zipfile.ZipFile(spath+"\\"+"pass.zip","w",zipfile.ZIP_DEFLATED) #压缩
zipfile.write(spath+"\pass.txt")
zipfile.close()
"""
savepath="C:\\Users\\ysongyang\\PycharmProjects\\password"
zipfile=zipfile.ZipFile(savepath+"\\"+"pass.zip","r") #解压缩
for  filename  in zipfile.namelist(): #遍历每一个文件
    data=zipfile.read(filename) #读取文件
    print(filename) #打印文件名
    filelist=filename.split("/")

    savefile=open(savepath+"\\ac\\"+filelist[len(filelist)-1],"wb")
    savefile.write(data) #压缩的数据取出并写入
    savefile.close()
