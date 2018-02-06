import requests
from bs4 import BeautifulSoup
import os, shutil
import time
import random


class BeautyGirl:
    #  获取一个页面的html代码
    def get_html(self, girl_url):
        girl_html = requests.get(girl_url).text
        return girl_html

    # 获取传入页号的url得到当前页面的全部组图url，并去重，按顺序存入list_url

    def get_url(self, page_pic_url):
        html = self.get_html(page_pic_url)
        soup = BeautifulSoup(html, "lxml")
        list_url = []
        for i in soup.select("#pins li a"):
            list_url.append(i.get("href"))
        list_url = sorted(set(list_url), key=list_url.index)
        return list_url

    # 根据传入的单组图取他一共有多少页（即有多少张图片）

    def get_num(self, url):
        html = self.get_html(url)
        soup = BeautifulSoup(html, "lxml")
        num = soup.select(".pagenavi a")[4].string
        return num

    # 得到一组图里面的每张图片的链接

    def pic_url(self, url):
        html = self.get_html(url)
        soup = BeautifulSoup(html, "lxml")
        pic_url = soup.select(".main-image img")[0].get("src")
        return pic_url


# 构造请求头

def get_header(Img_url, user_agent):
    header = {

        "Referer": Img_url,
        'User-Agent': user_agent
    }
    return header


# 根据每张图片所在组的代号，返回保存图片的名字

def create_folder(x, name):
    if not os.path.isdir(path + name):  # 先判断改文件夹是否存在
        x = 1
        os.mkdir(path + name)
    pic_name = name + "_" + str(x) + ".jpg"
    return path + name + "/" + pic_name


# 下载函数


def download(girl_url):
    num = 1  # 图片的名字从1开始起
    connect_num = 5  # 当连接超时时，最多重连的次数
    folder_name = girl_url.split("m/")[1]  # 根据传入的组图的url获取该组图的代号，作为文件夹的名字和图片的一部分名字
    url_num = girl.get_num(girl_url)  # 获取该组图共有多少张图片
    for j in range(1, int(url_num) + 1):  # 循环下载图片
        url = girl_url + "/" + str(j)  # 获取该组图的所有图片所在网页的url
        referer_url = girl_url + "/" + str(j - 1)  # 获取该组图上一张图片所在网页的url（为了构造请求头）
        condition = True  # 设置一个标识,当没抛出异常时，变为False，退出循环，否则就尝试再次连接
        while condition and connect_num > 0:
            try:
                # 使用timeout参数设置超时时间
                html = requests.get(girl.pic_url(url), headers=get_header(referer_url, random.choice(user_agent)),
                                    timeout=500).content
                with open(create_folder(num, folder_name), "wb") as f:
                    print("正在下载：" + url)
                    f.write(html)
                    num += 1
                    condition = False
            except requests.exceptions.RequestException:
                print("正在尝试第" + str(6 - connect_num) + "次连接！")
                connect_num -= 1
    # 当5次连接后还是抛出timeout错误，就删除该组图的文件夹，并将该组图的代号记录进Timeout.txt，待以后下载
    if connect_num == 0:
        shutil.rmtree("F:/single_welfare/" + folder_name)
        with open("F:/single_welfare/Timeout.txt", "a") as f:
            f.write(folder_name + "\n")
    # 一组图下载完后记录下它的代号，以便下次下载时去重
    else:
        with open("F:/single_welfare/page.txt", "a") as f:
            f.write(folder_name + "\n")
    # 下载完一组图后，设置5秒休眠时间
    time.sleep(5)


# 图片保存地址


path = "F:/single_welfare/"
if not os.path.isdir(path):
    os.mkdir(path)
Url = "http://www.mzitu.com/"
girl = BeautyGirl()  # 实例化BeautyGirl类
# 多设置几个浏览器标识，然后随机选择
user_agent = [r"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0",
              r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063",
              r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"]

for i in range(1, 155):
    url = Url + "page/" + str(i)  # 每一页的url
    all_girl_url = girl.get_url(url)
    page_num = list(map(lambda x: x.split("m/")[1], all_girl_url))  # 获取all_girl_url中每组图的代号，与page.txt文件判断然后去重
    if not os.path.isfile(path + "page.txt"):  # 检测page.txt是否存在，不存在则创建
        with open(path + "page.txt", "w") as f:
            pass
    with open(path + "page.txt", "r") as f:  # 打开page.txt，并读取全部内容
        list_page = f.read()
        for girl_num, one_girl_url in zip(page_num, all_girl_url):
            if girl_num not in list_page:  # 当当前组图的代号不在page.txt中时，执行下载函数
                download(one_girl_url)
