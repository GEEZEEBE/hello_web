from selenium import webdriver
from pymongo import MongoClient
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


def DBinsert(data):
    db_url = "mongodb://172.17.0.1:27017/"
    db_name = "webscrapDB"
    collection_name = "workorkrCollection"

    with MongoClient(db_url) as client:
        db = client[db_name]
        if (collection_name not in db.list_collection_names()):
            db.create_collection(collection_name)

        result = db[collection_name].insert_one(data)
        print(result.inserted_id)


def scraping_workorkr():
    path = 'driver/chromedriver'
    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    with webdriver.Chrome(executable_path=path, options=options) as driver:
        driver.get(url="https://www.work.go.kr/empInfo/indRev/indRevMain.do")   # 4차산업혁명
        time.sleep(3)

        for page in range(1, 25):
            input_page = driver.find_element(By.XPATH, "//*[@id='currentPageNo']")
            input_page.clear()
            input_page.send_keys(str(page) + Keys.ENTER)
            time.sleep(4)

            companies = [e.text for e in driver.find_elements(By.XPATH, "//a[@class='cp_name']")]
            infos = [e.text for e in driver.find_elements(By.XPATH, "//div[@class='cp-info-in']")]
            tasks = [e.text.split(":")[1].lstrip() for e in driver.find_elements(By.XPATH, "//p[@class='mt10']")]
            careers = [e.text for e in driver.find_elements(By.XPATH, "//div/p[2]/em[1]")]
            edu_levels = [e.text for e in driver.find_elements(By.XPATH, "//div/p[2]/em[2]")]
            locations = [e.text for e in driver.find_elements(By.XPATH, "//div/p[2]/em[3]")]
            salaries = [e.text for e in driver.find_elements(By.XPATH, "//td[4]/div/p[1]")]
            work_times = [e.text for e in driver.find_elements(By.XPATH, "//td[4]/div/p[3]")]
            reg_dates = [e.text.split('\n')[0] for e in driver.find_elements(By.XPATH, "//td[5]/div/p[2]")]
            due_dates = []
            for e in driver.find_elements(By.XPATH, "//td[5]/div/p[2]"):
                due_dates.append('') if e.text.find('\n') == -1 else due_dates.append(e.text.split('\n')[1])

            for values in zip(companies, infos, tasks, careers, edu_levels, locations, salaries, work_times, reg_dates, due_dates):
                keys = ['company', 'info', 'task', 'career', 'edu_level', 'location', 'salary', 'work_time', 'reg_date', 'due_date']
                data = dict()
                for k, v in zip(keys, values):
                    data[k] = v
                print(data)
                DBinsert(data)


if __name__ == "__main__":
    scraping_workorkr()
