import requests
import bs4
import warnings

warnings.filterwarnings('ignore')


def read_contents_from_readhub():
    res = requests.get('https://readhub.me/')
    soup = bs4.BeautifulSoup(res.text)
    items = soup.select('div[class="topicItem___3YVLI"]')
    contents = {each_item.select('h2 span')[0].text: each_item.select('div[class="summary___1i4y3"] div')[0].text[0:80]
                + '...\n' + each_item.select('a')[0].get('href')
                for each_item in items}
    # contents = {each_item.select('h2 span')[0].text: each_item.select('a')[0].get('href')
    #             for each_item in items}

    return contents


if __name__ == '__main__':
    cts = read_contents_from_readhub()

    for k, v in cts.items():
        print("%s:\n%s" % (k, v))
        print('----------------------------------------')
