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

rank = []
song_title = []
song_id = []

if req.status_code == requests.codes.ok:
    soup = BeautifulSoup(req.text, 'lxml')
    div = soup.find_all('td', 'check')
    songs = soup.select('div.ellipsis.rank01 > span > a')

    for i, music in enumerate(songs):
        rank.append(i+1)
        song_title.append(music['title'].strip(" 재생"))
        song_id.append(music['href'].strip("javascript:melon.play.playSong('19041401',").replace(");", ''))





#코랩 실행용
!pip install selenium
!apt-get update
!apt install chromium-chromedriver

# 이 부분은 처음 한번만 실행
# 코드 수정 - "The reason is that the last Ubuntu update update supports chromium driver just via snap."
# 최근 우분투 업데이트에서 크롬 드라이버 설치를 snap을 이용해서만 하도록 바뀜
# 고로 snap 없이 설치하는 아래 우회 코드로 변경
# 출처 : https://colab.research.google.com/drive/1cbEvuZOhkouYLda3RqiwtbM-o9hxGLyC
# 출처2 : https://stackoverflow.com/questions/75155063/selenium-use-chrome-on-colab-got-unexpectedly-exited

%%shell
# Ubuntu no longer distributes chromium-browser outside of snap
#
# Proposed solution: https://askubuntu.com/questions/1204571/how-to-install-chromium-without-snap

# Add debian buster
cat > /etc/apt/sources.list.d/debian.list <<'EOF'
deb [arch=amd64 signed-by=/usr/share/keyrings/debian-buster.gpg] http://deb.debian.org/debian buster main
deb [arch=amd64 signed-by=/usr/share/keyrings/debian-buster-updates.gpg] http://deb.debian.org/debian buster-updates main
deb [arch=amd64 signed-by=/usr/share/keyrings/debian-security-buster.gpg] http://deb.debian.org/debian-security buster/updates main
EOF

# Add keys
apt-key adv --keyserver keyserver.ubuntu.com --recv-keys DCC9EFBF77E11517
apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 648ACFD622F3D138
apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 112695A0E562B32A

apt-key export 77E11517 | gpg --dearmour -o /usr/share/keyrings/debian-buster.gpg
apt-key export 22F3D138 | gpg --dearmour -o /usr/share/keyrings/debian-buster-updates.gpg
apt-key export E562B32A | gpg --dearmour -o /usr/share/keyrings/debian-security-buster.gpg

# Prefer debian repo for chromium* packages only
# Note the double-blank lines between entries
cat > /etc/apt/preferences.d/chromium.pref << 'EOF'
Package: *
Pin: release a=eoan
Pin-Priority: 500


Package: *
Pin: origin "deb.debian.org"
Pin-Priority: 300


Package: chromium*
Pin: origin "deb.debian.org"
Pin-Priority: 700
EOF

# Install chromium and chromium-driver
apt-get update
apt-get install chromium chromium-driver

# Install selenium
pip install selenium



import selenium
from IPython.display import display
from selenium import webdriver # webdriver를 이용해 해당 브라우저를 열기 위해
from selenium.webdriver.chrome.service  import Service
from selenium.webdriver import ActionChains # 일련의 작업들을(ex.아이디 입력, 비밀번호 입력, 로그인 버튼 클릭...) 연속적으로 실행할 수 있게 하기 위해
from selenium.webdriver.common.keys import Keys # 키보드 입력을 할 수 있게 하기 위해
from selenium.webdriver.common.by import By # html요소 탐색을 할 수 있게 하기 위해
from selenium.webdriver.support.ui import WebDriverWait # 브라우저의 응답을 기다릴 수 있게 하기 위해
from selenium.webdriver.support import expected_conditions as EC # html요소의 상태를 체크할 수 있게 하기 위해


#Colab에선 웹브라우저 창이 뜨지 않으므로 별도 설정한다.
options = webdriver.ChromeOptions()
options.add_argument('--headless')        # Head-less 설정
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
genreDriver = webdriver.Chrome(options=options)


genres = []
artists = []

for j in song_id:
    genreURL = f'https://www.melon.com/song/detail.htm?songId={j}'
    genreDriver.get(genreURL)
    songDetail = genreDriver.page_source
    genreSoup = BeautifulSoup(songDetail, 'lxml')

    genre = str(genreSoup.select('div.meta > dl.list > dd'))
    artist = str(genreSoup.select('div.artist > a'))

    genre = re.sub("(<dd>|</dd>|amp;)", '', genre).split(', ')
    singer = re.search('<span>(.+?)</span>', artist).group(1)

    genres.append(genre[2])
    artists.append(singer)

data = []

for i in range(100):
    data.append([rank[i], song_title[i], artists[i], genres[i], song_id[i]])

df = pd.DataFrame(data, columns=['rank', 'song_title', 'artist', 'genre', 'song_id'])

pd.set_option('display.max_row', 500)

df