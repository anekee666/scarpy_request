import requests
from lxml import html
from urllib.parse import urljoin
from pymongo import MongoClient


def insert_to_db(list_currencies):
    client = MongoClient(
        "mongodb://user:IN3QeWTvtxR7kKUL@cluster0-shard-00-00.vb8yc.mongodb.net:27017,cluster0-shard-00-01.vb8yc.mongodb.net:27017,cluster0-shard-00-02.vb8yc.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-xoolvm-shard-0&authSource=admin&retryWrites=true&w=majority")
    db = client["books"]
    collection = db["book"]
    collection.insert_many(list_currencies)
    client.close()


def get(list_elements):
    try:
        return list_elements.pop(0)
    except:
        return ''


all_books = []


def scrape(url):
    resp = requests.get(url=url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
    })

    tree = html.fromstring(html=resp.content)

    books = tree.xpath("//html/body/div/div/div/div/section/div/ol/li")
    for book in books:
        c = {
              "_id": get(book.xpath(".//article/div[1]/a/img/@src")),
              'name': urljoin(url,get(book.xpath(".//div/a/@href"))),
        }
    #
        all_books.append(c)

    next_page = tree.xpath('//li[@class="next"]/a/@href')

    # if len(next_page) != 0:
    #     next_page_url = urljoin(base=url, url=next_page[0])
    #     print(next_page_url)
    #     scrape(url=next_page_url)



scrape(url="https://books.toscrape.com/")
insert_to_db(all_books)
# print(len(all_books))