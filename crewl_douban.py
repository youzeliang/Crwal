import requests
import xlwt, xlrd
from bs4 import BeautifulSoup
import re
import time


def get_html(url):
    return requests.get(url).text


def get_all_movie(html):
    soup = BeautifulSoup(html, 'lxml')
    # Movie_url = soup.select("ol a") 获取的方式很多，这种需要去重
    movie_url = soup.select(".pic a")
    url_list = []
    for i in movie_url:
        url_list.append(i.get("href"))
    return url_list


def get_comment(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    text = soup.select(".comment-item p", limit=1)[0].get_text()  # limit限制匹配数量
    pattern = re.compile(r"\S+")
    results = re.findall(pattern, text)[0]
    return results


def get_message(url):
    all = []
    try:
        html = get_html(url)
        soup = BeautifulSoup(html, 'lxml')
        name = soup.select("h1 span")[0].get_text()
        all.append(name)
        scout = soup.select(".ll.rating_num")[0].get_text()
        all.append(scout)
        info = soup.select("#info .attrs")
        director = info[0].get_text()
        all.append(director)
        screenwriter = info[1].get_text()
        all.append(screenwriter)
        actor = info[2].get_text()
        all.append(actor)
        all_types = soup.find_all(attrs={"property": "v:genre"})
        types = ""
        for i in range(len(all_types)):
            if i == len(all_types) - 1:
                types += all_types[i].get_text()
            else:
                types = types + all_types[i].get_text() + "/"
        all.append(types)
        all_time = soup.find_all(attrs={"property": "v:initialReleaseDate"})
        times = ""
        for i in range(len(all_time)):
            if i == len(all_time) - 1:
                times += all_time[i].get_text()
            else:
                times = times + all_time[i].get_text() + "/"
        all.append(times)
        all_comment = soup.select("#comments-section h2 a")[0]
        pattern = re.compile(r"\d+")
        results = re.findall(pattern, all_comment.get_text())[0]
        all.append(results)
        comment_url = all_comment.get("href")
        comment = get_comment(comment_url)
        all.append(comment)
        pic = soup.select("#mainpic img")[0].get("src")
        all.append(pic)
    except IndexError:
        return
    return all


def set_style():
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = "SimSun"
    font.height = 240  # 字体大小
    font.bold = True  # 是否加粗
    font.colour_index = 2  # 字体颜色(0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta)
    style.font = font
    alignment = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_CENTER  # 水平居中
    alignment.vert = xlwt.Alignment.VERT_CENTER  # 垂直居中
    style.alignment = alignment
    return style


f = xlwt.Workbook()
sheet1 = f.add_sheet(u"豆瓣电影")
row = [u"片名", u"评分", u"导演", u"编剧", u"主演", u"类型", u"上映时间", u"评论人数", u"热门评论", u"海报链接"]
for i in range(0, len(row)):
    sheet1.write(0, i, row[i], set_style())
f.save(r"豆瓣1.xls")

url_list = []
flag = 0
for i in range(10):
    url = "https://movie.douban.com/top250" + "?start=" + str(flag) + "&filter="
    flag += 25
    url_list.extend(get_all_movie(get_html(url)))
for i in range(len(url_list)):

    message = get_message(url_list[i])
    if message is not None:
        for j in range(len(row)):
            sheet1.write(i + 1, j, message[j])
        f.save(r"豆瓣1.xls")
        print(message)
