#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import re
import json
from bs4 import BeautifulSoup
from datetime import datetime


# Get website url


def get_url(url):
    res = requests.get(url)
    res.encoding = 'utf-8'
    html_sample = res.text
    soup = BeautifulSoup(html_sample,'html.parser')
    return soup


def get_content(url):
    soup = get_url(url)
    for news in soup.select('.news-item'):
        if len(news.select('h2')) > 0:
            h2 = news.select('h2')[0].text
            time = news.select('.time')[0].text
            a = news.select('a')[0]['href']
            return time, h2, a


def get_title(url):
    soup = get_url(url)
    title = soup.select('#artibodyTitle')[0].text
    return title


def get_source(url):
    soup = get_url(url)
    time_source = soup.select('.time-source')[0].contents[0].strip()
    dt = datetime.strptime(time_source.encode('utf-8'), '%Y年%m月%d日%H:%M')
    source = soup.select('.time-source span a')[0].text
    return dt, source


commentsURL = 'http://comment5.news.sina.com.cn/page/info?version=1&format=js&channel=gn&newsid=comos-fykpzey3694410&group=&compress=0&ie=utf-8&oe=utf-8&page=1&page_size=20'


def get_comments(newsurl):
    news = re.search('doc-i(.+).shtml', newsurl)
    newsid = news.group(1)
    print newsid
    comment = requests.get(commentsURL.format(newsid))
    print comment
    result = json.loads(comment.text.strip('var data='))
    total_comments = result['result']['count']['total']
    print total_comments

get_content('http://news.sina.com.cn/china/')
get_title('http://news.sina.com.cn/c/gat/2017-09-01/doc-ifykpzey3694410.shtml')
get_title('http://news.sina.com.cn/o/2017-09-01/doc-ifykpuui0344931.shtml')
get_source('http://news.sina.com.cn/c/gat/2017-09-01/doc-ifykpzey3694410.shtml')
get_comments('http://news.sina.com.cn/c/nd/2017-09-01/doc-ifykpuui0320241.shtml')