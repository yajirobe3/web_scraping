# coding: UTF-8
import urllib.request, urllib.error
from bs4 import BeautifulSoup
from datetime import datetime
import schedule
import pandas as pd
import time

def task():
    # 現在時刻を取得
    nowTime = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    url = "http://news.livedoor.com/%E5%AE%87%E5%AE%99/topics/keyword/32398/"
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, "html.parser")

    # コンテンツを取得
    contents = soup.find_all("li")

    columns = ["GetInformationDate", "Topic", "Link"]
    df = pd.DataFrame(columns = columns)

    print(nowTime)
    for content in contents:
        topic = content.find('h3')
        if (topic != None):
            link = content.find('a')
            detailLink = link.get('href')
            print('Title :' + str(topic.text) + 'Link :' + detailLink)
            _csv = pd.Series([nowTime, str(topic.text), detailLink], columns)
            df = df.append(_csv, columns)

    # csv出力
    csvFile = "result.csv"
    df.to_csv(csvFile, encoding = 'utf-8-sig')

if __name__ == '__main__':
    # 10分毎にjobを実行
    schedule.every(10).minutes.do(task)
    # 毎時間ごとにjobを実行
    #schedule.every().hour.do(task)
    # AM10:30にjobを実行
    #schedule.every().day.at("10:30").do(task)
    # 月曜日にjobを実行
    #schedule.every().monday.do(task)
    # 水曜日の13:15にjobを実行
    #schedule.every().wednesday.at("13:15").do(task)

    while True:
        schedule.run_pending()
        time.sleep(1)
