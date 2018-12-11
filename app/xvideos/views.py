import urllib
import re
import requests

import json

from . import xvideos
from flask import render_template, request, jsonify
from bs4 import BeautifulSoup


class Video:

    def __init__(self, title, img, url, duration):
        self.title = title
        self.img = img
        self.url = url
        self.duration = duration

    def __jsonencode__(self):
        """
        方式一：
        Serialize the object custom object
        :return:
        """
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def to_json(self):
        """
        方式二：
        Serialize the object custom object
        :return:
        """
        video = {
            'title': self.title,
            'img': self.img,
            'url': self.url,
            'duration': self.duration
        }
        return video


class AdvancedJSONEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, list):
            return list(o)
        return json.JSONEncoder.default(self, o)


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


@xvideos.route('/index.json', methods=['GET'])
def indexJson():
    """
    首页数据
    :return:
    """

    # print(request.args)

    hostname = 'https://www.xvideos.com'

    k = request.args.get('k')

    page = request.args.get('p')

    if k is not None:
        keywords = urllib.parse.unquote(k)
        print(keywords)
        hostname = "{}?k={}".format(hostname, keywords);

    if page is not None:
        hostname = "{}?p={}".format(hostname, page);

    if page is not None and k is not None:
        hostname = "{}?k={}&p={}".format(hostname, k, page)

    print(hostname)

    r = requests.get(hostname)
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
        video = Video(mv_title, mv_img, mv_url, duration)
        videos.append(video)

    return json.dumps(videos, default=lambda obj: obj.__dict__)


@xvideos.route('/ok.json')
def ok():
    videos = list()

    # videos.append(Video('sd', 'sds', 'sds', 'sdsd').to_json())

    videos.append(Video('sd1', 'sds', 'sds', 'sdsd'))
    videos.append(Video('sd2', 'sds', 'sds', 'sdsd'))
    videos.append(Video('sd3', 'sds', 'sds', 'sdsd'))
    videos.append(Video('sd4', 'sds', 'sds', 'sdsd'))
    videos.append(Video('sd5', 'sds', 'sds', 'sdsd'))

    # return json.dumps(videos, default=lambda obj: obj.__dict__)
    # return jsonify({video.to_json() for video in videos})
    # return jsonify({"results": video.to_json() for video in videos})

    # return json.dumps(videos)
    # return jsonify({'result: '})

    print(len(videos))
    for v in videos:
        print(v)
    # return jsonify({'results': video.to_json() for video in videos});
    #  有问题.
    return jsonify({'videos': video.to_json() for video in videos});


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


@xvideos.route("/detail.json")
def detail_json():
    """
    视频详情信息
    :return:
    """
    url = request.args.get('url')
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    video_title = ''
    video_real_url = ''
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

    return jsonify(video_title=video_title, video_real_url=video_real_url)
