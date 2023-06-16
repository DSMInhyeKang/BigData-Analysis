# 라이브러리, 프레임워크
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from collections import Counter
import re
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm


#멜론 차트(월간)
url ='https://www.melon.com/chart/month/index.htm'

header = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
req = requests.get(url, headers=header)
print(req.status_code)

if req.status_code == requests.codes.ok:
    soup = BeautifulSoup(req.text, 'lxml')
    div = soup.find_all('td', 'check')
    songs = soup.select('div.ellipsis.rank01 > span > a')

    chart = []

    for i, music in enumerate(songs):
        chart.append([i+1, music['title'].strip(" 재생"), (music['href']).strip("javascript:melon.play.playSong('19041401',").replace(");", '')])

    df = pd.DataFrame(chart, columns=['rank', 'song_title', 'song_id'])