# coding=utf-8

from PIL import  Image



"""判断JPG文件下载是否完整 
"""
def is_valid_jpg(jpg_file):
    if jpg_file.split('.')[-1].lower() == 'jpg':
        with open(jpg_file, 'rb') as f:
            f.seek(-2, 2)
            return f.read() == '\xff\xd9' #判定jpg是否包含结束字段
    else:
        return True

def is_jpg(filename):
    try:
        i=Image.open(filename)
        return i.format =='JPEG'
    except IOError:
        return False

#输入参数为文件路径
def IsValidImage(pathfile):
  bValid = True
  try:
    Image.open(pathfile).verify()
  except:
    bValid = False
  return bValid

if __name__ == '__main__':
    print(is_jpg('images/5.jpg'))