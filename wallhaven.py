'''
Wallhaven爬虫

URL：
    主页：https://wallhaven.cc
    图片网页链接：https://wallhaven.cc/w/r2qqlj    (r2qqlj:图片名)    https://whvn.cc/ey6rdo
    高清图：https://w.wallhaven.cc/full/r2/wallhaven-r2qqlj.jpg       （r2:图片名前两位）
    搜索标签：https://wallhaven.cc/search?q=id:1&ref=fp    （id：标签id）
    最新：https://wallhaven.cc/latest
    最热：https://wallhaven.cc/toplist
    随机：https://wallhaven.cc/random
    翻页：https://wallhaven.cc/search?q=id%3A1&ref=fp&page=2  (关键字)

'''

from requests import get
from json import loads
from contextlib import closing
from filetype import guess
from os import rename
from os import makedirs
from os.path import exists
import time
from lxml import etree


'''
  文件下载模块 Download()
  接收参数：
    file_url: 文件url
    file_name: 文件完整路径名
    nowCount: 当前下载文件数统计
    allCount: 总文件数
'''


def Download(file_url, file_name, nowCount, allCount):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}
    with (closing(get(file_url, headers=headers))) as response:
        with(open(file_name, "wb"))as file:
            file.write(response.content)
    a = int((nowCount/allCount)*50)
    print("\r 正在下载 %s ......" % (file_url))
    print("\r 总进度: [%s%s%s]   %d/%d" % (
          "="*a, ">", " "*(50-a), nowCount, allCount), end="")



'''
  爬虫抓取图片模块
'''


def Crawler(wtype, page):
    url = "https://wallhaven.cc/"
    photoIDs = list()
    jpgs = list()
    pngs = list()
    print(type(photoIDs))
    if wtype == '1':
        url += "latest"
    elif wtype == '2':
        url += "toplist"
    else:
        url += "random"
    for i in range(int(page)):
        rurl = url
        if i != 0:
            rurl = url + "?page="+str(i + 1)
        print(rurl)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}
        response = get(rurl, headers=headers)
        html = etree.HTML(response.text)
        jpgs.extend(html.xpath(
            "//figure[not(./div/span[@class='png'])]/@data-wallpaper-id"))  # 获取图片ID
        pngs.extend(html.xpath(
            "//figure[./div/span[@class='png']]/@data-wallpaper-id"))
    photoIDs.append(jpgs)
    photoIDs.append(pngs)
    # 所有图片张数
    allCount = len(jpgs)+len(pngs)
    # 已下载计数
    count = 1
    photoType = ".jpg"
    for pid in photoIDs:

        for id in pid:

            # 创建一个文件夹存放我们下载的图片
            if not exists('./imgs/' + str(wtype)):
                makedirs('./imgs/' + str(wtype))
            # 准备下载的图片链接
            photoUrl = "https://w.wallhaven.cc/full/" + \
                id[:2] + "/wallhaven-" + id + photoType
            # 准备保存到本地的完整路径
            photoName = './imgs/' + str(wtype) + '/' + id + photoType
            Download(photoUrl, photoName, count, allCount)
            count += 1
            # time.sleep(1)

        photoType = ".png"
    print("\n\r 下载完成！")


if __name__ == "__main__":
    wtype = input("请选择分类：\n\r1.最新 \n\r2.最热 \n\r3.随机\n")
    page = input("请输入页数（每页24张）：")
    Crawler(wtype, page)
