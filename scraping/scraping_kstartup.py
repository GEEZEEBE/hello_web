import requests
from bs4 import BeautifulSoup
from time import strftime
from datetime import datetime
from pymongo import MongoClient


def DBinsert(data):
    db_url = "mongodb://172.17.0.1:27017/"
    db_name = "webscrapDB"
    collection_name = "kstartupCollection"

    with MongoClient(db_url) as client:
        db = client[db_name]
        if (collection_name not in db.list_collection_names()):
            db.create_collection(collection_name)

        result = db[collection_name].insert_one(data)
        print(result.inserted_id)


def scraping_kstartup():
    url = f"https://www.k-startup.go.kr/common/announcement/announcementList.do?mid=30004&bid=701&searchAppAt=A"
    res = requests.get(url=url)
    # time.sleep(10)
    print(url)

    if res.status_code == 200:
        soup = BeautifulSoup(res.content, 'lxml')

    # print(soup.prettify())

    a_tags = soup.select('li h4 a')
    a_text = [a.text.strip() for a in a_tags]

    span_tags = soup.select('h4 span[class*="ann_list_group"]')
    span_text = [s.text for s in span_tags]

    li1_text, li2_text, li3_text = [], [], []
    ul_tags = soup.find_all('ul', class_='ann_list_info m0')
    for ul in ul_tags:
        li_tags = []
        for li in ul.find_all('li'):
            li_tags.append(li.text)
        li1_text.append(li_tags[0])
        li2_text.append(li_tags[1])
        li3_text.append(li_tags[2].split()[1])

    for values in zip(span_text, a_text, li1_text, li2_text, li3_text):
        keys = ['field', 'title', 'program', 'institute', 'due_date']
        data = dict()
        for k, v in zip(keys, values):
            data[k] = v
        print(data)
        DBinsert(data)

# print(datetime.now().strftime('%Y-%m-%d %a %H:%M:%s'))

if __name__ == "__main__":
    scraping_kstartup()

