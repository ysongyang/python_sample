# coding=utf-8
"""根据搜索词、缩放尺寸、页数下载百度图片"""

import re
import os
import urllib
import requests
from PIL import Image
import time


def getPageContent(keyword, page, n):
    page = page * n
    keyword = urllib.parse.quote(keyword, safe='/')
    url_begin = "http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word="
    url = url_begin + keyword + "&pn=" + str(page) + "&gsm=" + str(hex(page)) + "&ct=&ic=0&lm=-1&width=0&height=0"
    return url


def get_onepage_urls(onepageurl):
    try:
        html = requests.get(onepageurl).text
    except Exception as e:
        print(e)
        pic_urls = []
        return pic_urls
    pic_urls = re.findall('"objURL":"(.*?)",', html, re.S)
    return pic_urls


def down_pic(pic_urls, width):
    """给出图片链接列表, 下载所有图片"""
    for i, pic_url in enumerate(pic_urls):
        try:
            path = 'images/'
            folder = os.path.exists(path)
            if not folder:
                os.makedirs(path)
            #timeout 超时时间
            pic = requests.get(pic_url, timeout=20)
            string = path + str(i + 1) + '.jpg'
            with open(string, 'wb') as f:
                # print(string)
                f.write(pic.content)
                # 缩放图片
                zoom_image(string, i, width)
                # time.sleep(1)
                print('成功下载第%s张图片: %s' % (str(i + 1), str(pic_url)))
        except Exception as e:
            print('下载第%s张图片时失败: %s' % (str(i + 1), str(pic_url)))
            #os.remove(string)
            print(e)
            continue


def zoom_image(pic_url, i, width):
    try:
        # 判断图片是否存在
        if os.path.exists(pic_url):
            # 1 打开文件, 返回一个文件对象;
            im = Image.open(pic_url)
            # 2 获取图片尺寸
            width_im, height_im = im.size
            if (width_im > width):
                # 3. 缩放图片
                im.thumbnail((width, width))
                # 4.把缩放的图片保存;
                im.save('images/{}.jpg'.format(i + 1), 'jpeg')
    except Exception as e:
        print('缩放异常：%s' % str(e))

#判断是否图片
def is_jpg(filename):
    try:
        i = Image.open(filename)
        return i.format == 'JPEG'
    except IOError:
        return False

if __name__ == '__main__':
    keyword = input("请输入你要下载的图片关键词: ")  # 关键词, 改为你想输入的词即可, 相当于在百度图片里搜索一样
    width = int(input("请输入图片要缩放的宽度："))
    page_number = int(input("请输入你要采集的页数："))
    page_begin = 0
    image_number = 3
    all_pic_urls = []
    while 1:
        if page_begin > image_number:
            break
        print("第%d次请求数据", [page_begin])
        url = getPageContent(keyword, page_begin, page_number)
        onepage_urls = get_onepage_urls(url)
        page_begin += 1

        all_pic_urls.extend(onepage_urls)
    #下载图片
    down_pic(list(set(all_pic_urls)), width)
