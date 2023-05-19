import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from bs4 import BeautifulSoup
from tqdm import tqdm

cnt = []
re = []

lotto = {
    '1~10': 0,
    '11~20': 0,
    '21~30': 0,
    '31~40': 0,
    '41~50': 0
}

start = int(input("시작할 회차를 입력하세요 : "))
end = int(input("마지막 회차를 입력하세요 : "))

for i in range(start, end+1):
    url = f'https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&qvt=0&query={i}회%20로또당첨번호'
    req = requests.get(url)
    cnt.append(i)

    if req.status_code == requests.codes.ok:
        soup = BeautifulSoup(req.text, 'lxml')
        div = soup.find_all("div", { "class": "winning_number" })
        tmp = []

        for d in div:
            tmp = list(map(int, d.get_text().strip().split(" ")))
            re.append(tmp)
            
            for j in tmp:
                if j >= 1 and j <= 10:
                    lotto['1~10'] = (lotto['1~10'] + 1)
                elif j >= 11 and j <= 20:
                    lotto['11~20'] = (lotto['11~20'] + 1)
                elif j >= 21 and j <= 30:
                    lotto['21~30'] = (lotto['21~30'] + 1)
                elif j >= 31 and j <= 40:
                    lotto['31~40'] = (lotto['31~40'] + 1)
                else:
                    lotto['41~50'] = (lotto['41~50'] + 1)


lotteryList = pd.DataFrame.from_dict(lotto, orient='index', columns=['lottery winning nums'])

lotteryList.plot.pie(y='lottery winning nums', figsize=(8,8))
plt.annotate("most frequent number range", xy=(-0.8, 0.1), xytext=(-0.6, 0.7), arrowprops=dict(facecolor='yellow'))
plt.show()