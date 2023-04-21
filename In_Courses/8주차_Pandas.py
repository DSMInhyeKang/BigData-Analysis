import numpy as np
import pandas as pd
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import csv

# path = '/content/sample_data/california_housing_test.csv'
path = '/content/sample_data/california_housing_train.csv'
f = open(fr'{path}', encoding='cp949')
housing = pd.read_csv(f)

housing.info()
housing.describe()
housing.hist(bins=100, figsize=(20,15))

#plt.savefig("attribute_histogram_plots.png")
plt.show()

housing.plot(kind='scatter', x='longitude', y='latitude', alpha=0.1)

california_img = mpimg.imread('/content/drive/MyDrive/BigData Analysis/images/california.png')
plt.imshow(california_img, extent=[-124.55, -113.80, 32.45, 42.5], alpha=0.5)

housing.plot(kind='scatter', x='longitude', y='latitude', alpha=0.4,
             s=housing["population"]/100, #데이터 처리
             label="population", #범례(legend())
             figsize=(10,7), #맵의 사이즈
             c="median_house_value", #cbar = plt.colorbar()
             cmap=plt.get_cmap("jet"),
             colorbar=True,
             sharex=False
             )
plt.title('California housing prices')

california_img = mpimg.imread('/content/drive/MyDrive/BigData Analysis/images/california.png')
plt.imshow(california_img, extent=[-124.55, -113.80, 32.45, 42.5], alpha=0.9)

plt.show()



ax = housing.plot(kind="scatter", x="longitude", y="latitude", figsize=(25,7),
                  s=housing['population']/100, 
                  label="Population",
                  c="median_house_value", cmap=plt.get_cmap("jet"), 
                  colorbar=False, alpha=0.4,
                  )

plt.imshow(california_img, extent=[-124.55, -113.80, 32.45, 42.05], alpha=0.5,
           cmap=plt.get_cmap("jet"))

plt.ylabel("Latitude", fontsize=14)
plt.xlabel("Longitude", fontsize=14)

prices = housing["median_house_value"]
tick_values = np.linspace(prices.min(), prices.max(), 11)
cbar = plt.colorbar()    
cbar.ax.set_yticklabels([f"${round(v/1000)}k" for v in tick_values], fontsize=14)
cbar.set_label('Median House Value', fontsize=16)

plt.legend(fontsize=16)
plt.savefig("california_housing_prices_plot.png")
plt.show()