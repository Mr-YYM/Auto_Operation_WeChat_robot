import requests
import bs4

res = requests.get('https://readhub.me/')
soup = bs4.BeautifulSoup(res.text)

items = soup.select('div[class="topicItem___3YVLI"]')

for each_item in items:
    title = each_item.select('h2 span')[0]
    print(title.text)
