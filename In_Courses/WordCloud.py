import requests
from tqdm import tqdm
import numpy as np
from bs4 import BeautifulSoup
from collections import Counter
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
from PIL import Image
from wordcloud import ImageColorGenerator, STOPWORDS, WordCloud #stopwords: set of strings or None (불용어 처리)

# text = open(r'/content/drive/MyDrive/BigData Analysis/data/constitution.txt', 'rt').read()
# wordcloud = WordCloud().generate(text)

# plt.figure()
# plt.imshow(wordcloud, interpolation='bilinear') #보간법 - 수많은 점 평균화 - 픽셀 보정하여

# plt.axis("off")
# plt.show()



# wordcloud.to_file(fr'/content/drive/MyDrive/BigData Analysis/images/constitution.png')

# rank_lang_df = pd.DataFrame(
#     {
#         "language": ["JavaScript", "Python", "Java", "C/C++", "PHP", "C#", "Swift", "Kotlin"],
#         "million": [12.4, 9, 8.2, 6.3, 6.1, 6, 2.4, 2.3],        
#     }
# )

# fig = px.treemap(rank_lang_df, path=['language'], values='million')
# fig.show()



alice = np.array(Image.open(r'/content/drive/MyDrive/BigData Analysis/images/alice.png'))

stopwords = set(STOPWORDS)
stopwords.add("Alice")
stopwords.add("said")

text = open(r'/content/drive/MyDrive/BigData Analysis/data/alice.txt', 'rt').read()

wc = WordCloud(background_color="white", max_words=2000, mask=alice, width=1000, height=1000,
               stopwords=stopwords, contour_width=1, contour_color='steelblue')#,random_state=42)

wc.generate(text)

image_colors = ImageColorGenerator(alice)

plt.figure(figsize=[15, 20])
plt.imshow(wc, cmap=plt.cm.gray, interpolation='bilinear')
plt.axis("off")
plt.show()