#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import re
import json
from bs4 import BeautifulSoup
from datetime import datetime

commentsURL = 'http://comment5.news.sina.com.cn/page/info?version=1&format=js&channel=gn&newsid=comos-{}' \
              '&group=&compress=0&ie=utf-8&oe=utf-8&page=1&page_size=20'
# Get website url


def get_url(url):
    res = requests.get(url)
    res.encoding = 'utf-8'
    html_sample = res.text
    soup = BeautifulSoup(html_sample,'html.parser')
    return soup

# Get news content


def get_content(weburl):
    soup = get_url(weburl)
    for news in soup.select('.news-item'):
        if len(news.select('h2')) > 0:
            h2 = news.select('h2')[0].text
            time = news.select('.time')[0].text
            a = news.select('a')[0]['href']
            return time, h2, a

# Get news title


def get_title(url):
    soup = get_url(url)
    title = soup.select('#artibodyTitle')[0].text
    return title


def get_article(url):
    soup = get_url(url)
    article = ''.join([p.text.strip() for p in soup.select('#artibody p')[:-1]])
    return article
# Get news source and time


def get_source_time(url):
    soup = get_url(url)
    time_source = soup.select('.time-source')[0].contents[0].strip()
    # dt = datetime.strptime(time_source.encode('utf-8'), '%Y年%m月%d日%H:%M')
    return time_source


def get_source_news(url):
    soup = get_url(url)
    source = soup.select('.time-source span a')[0].text
    return source


def get_editor_name(url):
    soup = get_url(url)
    editor = soup.select('.article-editor')[0].text.encode('utf-8').strip('责任编辑：')
    return editor

# Get total comments for the news


def get_comments(newsurl):
    news = re.search('doc-i(.+).shtml', newsurl)
    newsid = news.group(1)
    comment = requests.get(commentsURL.format(newsid))
    result = json.loads(comment.text.strip('var data='))
    total_comments = result['result']['count']['total']
    return total_comments


# Put all those collected information into a dict

def get_news_detail(url):
    details = {}
    title = get_title(url)
    article = get_article(url)
    time = get_source_time(url)
    source = get_source_news(url)
    editor = get_editor_name(url)
    comments = get_comments(url)

    details['news title'] = title
    details['article'] = article
    details['time'] = time
    details['source'] = source
    details['editor'] = editor
    details['total comments'] = comments

    final_result = json.dumps(details,encoding="UTF-8", ensure_ascii=False, sort_keys=False, indent=4)

    print final_result



get_news_detail('http://news.sina.com.cn/c/nd/2017-09-03/doc-ifykqmrv8359781.shtml')
get_article('http://news.sina.com.cn/c/nd/2017-09-03/doc-ifykqmrv8359781.shtml')

