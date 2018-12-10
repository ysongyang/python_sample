import requests
from bs4 import BeautifulSoup
import re
from class_mysql import *


# 获取网页数据，伪装成浏览器
def gethtml(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'}
    req = requests.get(url, headers=headers)
    req.encoding = "GBK"
    html = req.text
    bf = BeautifulSoup(html, "html.parser")
    return bf


# 爬取标题
def gettitle(html):
    titlehtml = html.find_all("td", class_="td_title01")
    titletxt = str(titlehtml).strip()
    #p1 = r'shtml">(.*?)<f.*?<strong>(.*?)</strong>.*?</font>(.*?)</a>.* ?right">(.*?)</span>'
    p1 = r'<f.*?><strong>(.*?)</strong>.*?</font>'
    titles = re.compile(p1, re.S).findall(titletxt)
    #qi = list(titles[0])
    qi = titles[0]
    #qi[2] = ('期')
    #return ''.join(qi)
    return qi


# 爬取红色球
def getred(html):
    redhtml = html.find_all("li", class_="ball_red")
    redtxt = str(redhtml).strip()
    p1 = r'red">(.*?)</li>'
    reds = re.compile(p1, re.S).findall(redtxt)
    return ' '.join(reds)


# 爬取蓝色球
def getbule(html):
    bulehtml = html.find_all("li", class_="ball_blue")
    buletxt = str(bulehtml).strip()
    p1 = r'blue">(.*?)</li>'
    bules = re.compile(p1, re.S).findall(buletxt)
    return  ' '.join(bules)


# 获取所有url
def getlistnum(html):
    listnumhtml = html.find_all("div", class_="iSelectList")
    p1 = r'href="(.*?)">'
    listnums = re.compile(p1, re.S).findall(str(listnumhtml))
    return listnums[1:]


# 插入数据
def addChapterData(data):
    ms = MYSQL()
    stage = data['stage']
    # 如果数据不存在则进行插入数据
    if isNovelChapterId(stage) is None:
        sql = "insert into lottery_ssq (`stage`,`red`,`blue`) values ('%s' ,'%s' ,'%s')" % (
            data['stage'], data['red'], data['blue'])
        # print(sql)
        ms.ExecInsertQuery(sql)
    else:
        pass

# 判断数据是否存在
def isNovelChapterId(stage):
    ms = MYSQL()
    sql = "select * from lottery_ssq where stage = %s " % stage
    info = ms.ExecQuery(sql)
    return info


url = 'http://kaijiang.500.com/shtml/ssq/18139.shtml'


def main():
    html = gethtml(url)
    htmlurls = getlistnum(html)
    htmlurls.reverse() #数据反转
    #print(htmlurls)
    #exit('=============')
    for htmlurl in htmlurls:
        ssqhtml = gethtml(htmlurl)
        stage = gettitle(ssqhtml)
        red = getred(ssqhtml)
        blue = getbule(ssqhtml)
        print('期号：' + stage + '   红球：' + red + '   篮球：' + blue + '\n')
        if isNovelChapterId(stage) is None:
            data = {
                'stage':stage,
                'red':red,
                'blue':blue
            }
            #插入数据
            addChapterData(data)
            print(' stage %d 已入库！' % int(stage))
        # 写入txt文件
        #with open(r'ssq.txt', 'a') as f:
            #f.write(a + '  ' + b + '  ' + c + '\n')
            #f.close()


if __name__ == "__main__":
    main()
