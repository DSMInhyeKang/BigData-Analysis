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
from selenium.webdriver.common.by import By
import seaborn as sbn
from wordcloud import WordCloud
import konlpy
import PIL



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
artist_id = []

if req.status_code == requests.codes.ok:
    soup = BeautifulSoup(req.text, 'lxml')

    for i, singer in enumerate(soup.select('div.ellipsis.rank02 > a')):
        artist_id.append(singer['href'].strip("javascript:melon.link.goArtistDetail('").strip("');"))

    for i, music in enumerate(soup.select('div.ellipsis.rank01 > span > a')):
        rank.append(i+1)
        song_title.append(music['title'].strip(" 재생"))
        song_id.append(music['href'].strip("javascript:melon.play.playSong('19041401',").replace(");", ''))


#%%
#곡 정보(아티스트, 장르)
service = Service('../chromedriver/chromedriver.exe')
genreDriver = webdriver.Chrome(service=service)

for j in song_id:
    genreURL = f'https://www.melon.com/song/detail.htm?songId={j}'
    genreDriver.get(genreURL)
    songDetail = genreDriver.page_source
    genreSoup = BeautifulSoup(songDetail, 'lxml')

    genre = re.sub("(<dd>|</dd>|amp;)", '', str(genreSoup.select('div.meta > dl.list > dd'))).split(', ')
    genres.append(genre[2])

    artists.append(re.search('<span>(.+?)</span>', str(genreSoup.select('div.artist > a'))).group(1))
    

#%%
#아티스트 정보(활동)
artist_type = []
artist_id = list(set(artist_id))

for id in artist_id:
    artistURL = f'https://www.melon.com/artist/detail.htm?artistId={id}'
    artistReq = requests.get(artistURL, headers=header)
    artistSoup = BeautifulSoup(artistReq.text, 'lxml')
    
    artistInfo = re.sub("(<dd>|\r|\n|\t|<span class=\"bar\">|</span>|</dd>)", '', str(artistSoup.select('div.section_atistinfo03 > dl > dd'))).split(',')
    
    for type in artistInfo:
        if "남성" in type or "여성" in type:
            artist_type.append(type.strip())
    
#%%
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

genreDF = pd.DataFrame.from_dict([genreCounter])

display(genreDF)
#%%
#장르 파이 차트
plt.figure(figsize=(6.5,6.5))

genre_colors = ['#ff9999', '#ffc000', '#8fd9b6', '#d395d0', '#d5d5ea', '#97aeff', '#f8df81']
random.shuffle(genre_colors)

genre_label = list(genreCounter.keys())
genre_value = list(genreCounter.values())

plt.title('멜론 차트 Top 100 장르 분포표', fontdict={'fontsize':16,'fontweight':'bold','color':'green'}, loc='center', pad=15)
plt.pie(genre_value, explode=[0.1,0,0,0,0,0,0], labels=genre_label, colors=genre_colors, autopct='%1d%%', shadow=True, startangle=260, counterclock=False)
plt.annotate("인기 장르", xy=(-0.65,0.1), xytext=(-1.4, 0.7), arrowprops=dict(facecolor='yellow'))
plt.show()

#%%
#아티스트 유형 파악 막대 그래프
artistCounter = Counter(artist_type)
artistDF = pd.DataFrame.from_dict([artistCounter])
display(artistDF)

artist_color = ['salmon', 'darkorange', 'turquoise', 'gold']
random.shuffle(artist_color)

fig = plt.figure(facecolor='lightcyan')
ax = fig.add_subplot(1,1,1)
ax.set(ylim=[0,50], xlabel='아티스트 유형', ylabel='아티스트 유형별 수')
ax.tick_params(pad=8)
plots = sbn.barplot(data=artistDF)

xLabel = list(artistCounter.keys())
yLabel = list(artistCounter.values())

plt.title('멜론 차트 Top 100 아티스트 유형', fontdict={'fontsize':16, 'fontweight':'bold', 'color': 'darkgreen'}, loc='left', pad=15)
plt.bar(xLabel, yLabel, edgecolor='silver', color=artist_color, linewidth=1, tick_label=xLabel)

for bar in plots.patches:
    plt.annotate(format(bar.get_height(), '.0f'),(bar.get_x() + bar.get_width() / 2, bar.get_height()), ha='center', va='center',size=15, xytext=(0, 8),textcoords='offset points')
plt.show()

#%%
#월간 차트 Top 1~10 곡 댓글 수집
commentDriver = webdriver.Chrome(service=service)
comments = []

for i in range(1, 6):
    for id in song_id[:10]:
        commentURL = f'https://www.melon.com/song/detail.htm?songId={id}#cmtpgn=&pageNo={i}'
        commentDriver.get(commentURL)
        elemetns = commentDriver.find_elements(By.CSS_SELECTOR, "div.cmt_text")

        for e in elemetns:
            comments.append(e.text.strip('\n'))

commentDF = pd.DataFrame()
commentDF['comment_content'] = pd.DataFrame(comments).replace('[^가-힣]', ' ', regex = True)
display(commentDF)

#%%
#WordCloud 전용 DataFrame 생성
kkma = konlpy.tag.Kkma()
nouns = commentDF['comment_content'].apply(kkma.nouns).explode()
print(nouns)

wordDF = pd.DataFrame({'word': nouns})
wordDF['count'] = wordDF['word'].str.len()
wordDF = wordDF.query('count >= 2')
wordDF = wordDF.groupby('word', as_index = False).count().sort_values('count', ascending = False)

display(wordDF)


#%%
#WordCloud에 사용될 단어 dictionary로 변환 및 값 조정
dic_word = wordDF.set_index('word').to_dict()['count']

del dic_word['노래']
del dic_word['다운로드']
del dic_word['재생']

dic_word.update({'아이브':0,'언포기븐':0,'스파이시':0})
for wkey, wvalue in list(dic_word.items()):
    if '아이' == wkey or '이브' == wkey:
        print(wkey, wvalue)
        dic_word['아이브'] += wvalue
        del dic_word[wkey]
    elif '진스' == wkey or '뉴진' == wkey:
        dic_word['뉴진스'] = dic_word['뉴진스'] + wvalue
        del dic_word[wkey]
    elif '언포기' == wkey or '포기' == wkey:
        dic_word['언포기븐'] = dic_word['언포기븐'] + wvalue
        del dic_word[wkey]
    elif wkey == '하입':
        dic_word['하입보이'] = dic_word['하입보이'] + wvalue
        del dic_word[wkey]
    elif wkey == '세라핌':
        dic_word['르세라핌'] = (dic_word['르세라핌'] + wvalue)
        del dic_word[wkey]
    elif wkey =='재기':
        dic_word['사재기'] = dic_word['사재기'] + wvalue
        del dic_word[wkey]
for wkey, wvalue in list(dic_word.items()):
    if wkey == '버버' or wkey == '버버들' or wkey == '버들' or wkey == '네버':
        dic_word['네버버'] = dic_word['네버버'] + wvalue
        del dic_word[wkey]
    elif wkey == '스파' or wkey == '짱스파':
        dic_word['에스파'] = dic_word['에스파'] + wvalue
        del dic_word[wkey]
    elif wkey == '튜브':
        dic_word['유튜브'] = dic_word['유튜브'] + wvalue
        del dic_word[wkey]
    elif wkey == '프푸':
        dic_word['이프푸'] =  dic_word['이프푸'] + wvalue
        del dic_word[wkey]
    elif wkey == '파이':
        dic_word['파이팅'] = dic_word['파이팅'] + wvalue
        del dic_word[wkey]
    elif wkey == '스파이':
        dic_word['스파이시'] = dic_word['스파이시'] + wvalue
        del dic_word[wkey]


print(dic_word)
#%%
#멜론 월간 차트 Top 1~10 댓글 WordCloud
icon = PIL.Image.open('music.png')
img = PIL.Image.new('RGB', icon.size, (255,255,255))
img.paste(icon, icon)
img = np.array(img)

commentWC = WordCloud(random_state = 1234, font_path='C:\Windows\Fonts\malgun.ttf', width = 400, height = 400, background_color = 'snow', mask=img, colormap='inferno')


img_wordcloud = commentWC.generate_from_frequencies(dic_word)

plt.figure(figsize = (10, 10), facecolor='pink') # 크기 지정하기

plt.title('멜론 차트 Top 10 댓글 WordCloud', fontdict={'fontsize':25, 'fontweight':'bold', 'color': 'white'}, loc='center', pad=20)
plt.axis('off')
plt.imshow(img_wordcloud) # 결과 보여주기
plt.savefig('멜론_월간차트_Top10_워드클라우드') # 파일 저장
# %%