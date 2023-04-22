import csv
import matplotlib.pyplot as plt
import numpy as np

path = '/content/drive/MyDrive/BigData Analysis/data/202303_202303_연령별인구현황_월간-1.csv'
f = open(fr'{path}', encoding='cp949')
data = csv.reader(f)

result = []
city = input("사시는 동네 이름을 작성해주세요 :   ")
for row in data:
    if city in row[0]:
        for i in row[3:]:
            result.append(int(i.replace(',', '')))

print(result)

fig = plt.figure(facecolor='lightgray')
ax = fig.add_subplot(1,1,1)

ax.set(xlim=[0,100], ylim=[0,ylim], xlabel='Age', ylabel='Population')
plt.title("Population status by age", loc='center', pad=10)

plt.grid(True, axis='x', alpha=0.3, color='red', linestyle=':')
plt.grid(True, axis='y', color='gray', linestyle='--')

plt.annotate(f'local max({xpos}age)', xy=(xpos, ymax), xytext=(xpos+10, ymax+10), arrowprops=dict(facecolor='black', shrink=0.05))

plt.plot(result, color='blue', linestyle='-')

plt.show()