import urllib
import re
import requests

from . import xvideos
from flask import render_template, request
from bs4 import BeautifulSoup


class Video:

    def __init__(self, title, img, url, duration):
        self.title = title
        self.img = img
        self.url = url
        self.duration = duration


host = 'https://www.xvideos.com'


@xvideos.route('/index', methods=['GET'])
def index():
    """
    首页数据
    :return:
    """

    # print(request.args)

    k = request.args.get('k')

    page = request.args.get('p')

    page = 0
    k = '直播'

    if k is None:
        sea = host
    else:
        keywords = urllib.parse.unquote(k)
        print(keywords)
        sea = "{}?k={}".format(host, keywords);
    # 添加分页处理
    if page is not None and k is not None:
        sea = "{}&p={}".format(sea, page)
    else:
        sea = host

    r = requests.get(sea)
    # print(r.text)
    soup = BeautifulSoup(r.text, 'html.parser')
    # print(soup.title)

    # print(soup)
    # mv_list = soup.find('div', attrs={'class': 'mozaique'})
    # print(mv_list)

    videos = []
    result = soup.find_all('div', {'class': 'thumb-block'})

    # 枚举遍历, 下标及数据
    for index, item in enumerate(result):

        # 取元素下面的第一个a标签
        mv_url = item.find_all('a')[1].get('href')
        mv_title = item.find_all('a')[1].get('title')
        mv_img = item.find('img')['data-src']

        # 拼接视频地址.
        mv_url = '{}{}'.format(host, mv_url)
        duration = item.find('span', {'class': 'duration'}).get_text()
        # print(mv_title)
        if index == 0:
            print(index, duration, mv_title, mv_url, mv_img)
        video = Video(mv_title, mv_img, mv_url, duration)
        videos.append(video)
    return render_template('xvideos/xindex.html', videos=videos)


@xvideos.route("/detail")
def detail():
    url = request.args.get('url')
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    for script in soup.find_all('script'):
        # print(script)

        # 只获取视频地址脚本标签
        if re.search('setVideoUrlHigh', script.text):
            # print(script)
            # 通过正则获取文本内容
            # setVideoUrlHigh('')
            # group() 会显示原始字符.
            video_title = re.search("setVideoTitle\('(.*?)'\)", script.text).group(1)
            video_real_url = re.search("setVideoUrlHigh\('(.*?)'\)", script.text).group(1)
            print(video_title)
            print(video_real_url)

    return render_template('xvideos/detail.html', video_title=video_title, video_real_url=video_real_url)
