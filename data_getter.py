import requests
import bs4
import datetime
import warnings
import logging

warnings.filterwarnings('ignore')


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
                     'link': each_item.select('a')[0].get('href')
                }
            for each_item in items
        }

        return contents
    except Exception as exp:
        logging.error("发生了一个错误：%s" % exp)


if __name__ == '__main__':
    cts = read_contents_from_readhub()

    for k, v in cts.items():
        print("%s:\n%s" % (k, v))
        print('----------------------------------------')
