import requests
import bs4
import datetime
import warnings
import logging
import re
import db_process
import time
import random
from threading import Thread

warnings.filterwarnings('ignore')


def auto_update_db(interval):
    """
    自动更新数据库

    :param interval: int,分钟，默认15，每次爬取网页信息的时间间隔。
    """
    t = Thread(target=update_db, args=(interval,))
    t.start()


def update_db(interval=15):
    """
    定时从网站爬取信息并更新数据库中的内容

    :param interval: int,分钟，默认15，每次爬取网页信息的时间间隔。
    
    :return:
    """
    while 1:
        cts = read_contents_from_readhub()
        db_process.insert_cts_toDB(cts)
        time.sleep(interval * 60)


def get_send_cts(amount=2):
    """
    获取用来发送的内容信息。

    :param amount: 内容数量
    :return: 最终内容
    """
    cts = db_process.get_contents(10)  # get contents from database
    fmt_cts = get_formatted_contents(cts)  # formatting contents
    to_send_cts = random.sample(fmt_cts, amount)  # select final contents in a limited amount randomly
    return to_send_cts


# 获取源网站
def get_source_link(website):
    r = re.search('(http|https)(.+)(\.com|\.cn|\.org|\.net)', website)
    if r is not None:
        return r.group()
    else:
        return None


# 由于sina链接很长，url=部分才是有用的，利用这个函数提取sina链接中url=后面的部分
def is_sina_link(website):
    if re.search('url=', website) is not None:
        return re.split('url=', website)[1]
    else:
        return website


# 对内容进行格式化处理
def get_formatted_contents(contents):
    return ['【{t:s}】\n{content:s}\n{link:s}\n'.format(t=title, content=v['content'], link=v['link'])
            for title, v in contents.items()]


def read_contents_from_readhub():
    """
    从readhub上获取爬取新闻信息

    :return:一个字典，key为title（标题）：
    values分别有

    date_time（爬取时间）

    content（内容），

    link（内容网站），

    src_website（内容源网站）

    """
    try:
        res = requests.get('https://readhub.me/')
        soup = bs4.BeautifulSoup(res.text)
        items = soup.select('div[class="topicItem___3YVLI"]')
        contents = {
            each_item.select('h2 span')[0].text:
                {
                    'date_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
                    'content': each_item.select('div[class="summary___1i4y3"] div')[0].text,
                    'link': is_sina_link(each_item.select('a')[0].get('href'))
                }
            for each_item in items
        }

        for _, each_cts in contents.items():
            each_cts['src_website'] = get_source_link(each_cts['link'])

        return contents
    except Exception as exp:
        logging.error("发生了一个错误：%s" % exp)


if __name__ == '__main__':
    gfc = lambda contents: ['【{t:s}】\n{content:s}\n{link:s}\n'.format(t=title, content=v['content'], link=v['link'])
                            for title, v in contents.items()]
    raw = read_contents_from_readhub()
    cts = gfc(raw)
    for k in cts:
        print(k)
        print('----------------------------------------')
