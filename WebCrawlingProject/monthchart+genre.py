#%%
# 라이브러리, 프레임워크
import random
import requests
from bs4 import BeautifulSoup
from collections import Counter
import re
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import selenium
from IPython.display import display
from selenium import webdriver # webdriver를 이용해 해당 브라우저를 열기 위해
from selenium.webdriver.chrome.service  import Service


#%%
#멜론 차트(월간)
url ='https://www.melon.com/chart/month/index.htm'

header = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
req = requests.get(url, headers=header)
print(req.status_code)

rank = []
song_title = []
song_id = []
genres = []
artists = []

if req.status_code == requests.codes.ok:
    soup = BeautifulSoup(req.text, 'lxml')
    songs = soup.select('div.ellipsis.rank01 > span > a')

    for i, music in enumerate(songs):
        rank.append(i+1)
        song_title.append(music['title'].strip(" 재생"))
        song_id.append(music['href'].strip("javascript:melon.play.playSong('19041401',").replace(");", ''))


#%%
#곡 정보(아티스트, 장르)
service = Service('../chromedriver/chromedriver.exe')
driver = webdriver.Chrome(service=service)

for j in song_id:
    genreURL = f'https://www.melon.com/song/detail.htm?songId={j}'
    driver.get(genreURL)
    songDetail = driver.page_source
    genreSoup = BeautifulSoup(songDetail, 'lxml')

    genre = re.sub("(<dd>|</dd>|amp;)", '', str(genreSoup.select('div.meta > dl.list > dd'))).split(', ')

    genres.append(genre[2])
    artists.append(re.search('<span>(.+?)</span>', str(genreSoup.select('div.artist > a'))).group(1))


#가져온 모든 데이터 합치기
data = []

for i in range(100):
    data.append([rank[i], song_title[i], artists[i], genres[i], song_id[i]])

df = pd.DataFrame(data, columns=['rank', 'song_title', 'artist', 'genre', 'song_id'])
pd.set_option('display.max_row', 500)
display(df)

#%%
#장르 데이터 count
genreCounter = Counter(genres)

for key, value in list(genreCounter.items()):
    if value < 5:
        genreCounter['기타'] += genreCounter[key]
        del genreCounter[key]

#%%
#장르 파이 차트
plt.rc('font', family='Malgun Gothic')
plt.figure(figsize=(6,6))

genre_colors = ['#ff9999', '#ffc000', '#8fd9b6', '#d395d0', '#d5d5ea', '#97aeff', '#f8df81']
random.shuffle(genre_colors)

genre_label = list(genreCounter.keys())
genre_value = list(genreCounter.values())

plt.title('멜론 월간 차트 Top 100 장르 분포표', loc='center', pad=10)
plt.pie(genre_value, labels=genre_label, autopct='%1d%%', startangle=260, counterclock=False, colors=genre_colors)
plt.show()
# %%