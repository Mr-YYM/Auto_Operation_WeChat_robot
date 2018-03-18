import requests
import bs4
import datetime
import warnings
import logging
import re
import db_process
import time
from threading import Thread

warnings.filterwarnings('ignore')


def auto_update_db(interval):
    t = Thread(target=update_db, args=(interval,))
    t.start()


def update_db(interval=15):
    while 1:
        cts = read_contents_from_readhub()
        db_process.insert_cts_toDB(cts)
        time.sleep(interval * 60)


def get_send_cts(amount=2):
    cts = db_process.get_contents(amount)  # insert contents into database and get addition contents
    fmt_cts = get_formatted_contents(cts)  # formatting contents
    to_send_cts = get_limited_amount_contents(fmt_cts, 2)  # final contents in a limited amount
    return to_send_cts


def get_source_link(website):
    r = re.search('(http|https)(.+)(\.com|\.cn|\.org|\.net)', website)
    if r is not None:
        return r.group()
    else:
        return None


def is_sina_link(website):
    if re.search('url=', website) is not None:
        return re.split('url=', website)[1]
    else:
        return website


def get_formatted_contents(contents):
    return ['【%s】\n%s\n%s\n' % (title, v['content'], v['link'])
            for title, v in contents.items()]


def get_limited_amount_contents(contents, amount=None):
    if amount is None or len(contents) < amount:
        return contents
    else:
        return [contents[t] for t in range(amount)]


def read_contents_from_readhub():
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
    gfc = lambda contents: ['【%s】\n%s\n%s\n' % (title, v['content'], v['link']) for title, v in contents.items()]
    raw = read_contents_from_readhub()
    cts = gfc(raw)
    for k in cts:
        print(k)
        print('----------------------------------------')
