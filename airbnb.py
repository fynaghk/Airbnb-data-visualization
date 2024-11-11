import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium

data = pd.read_csv('/content/Airbnb_Open_Data.csv')

# Çatışmayan dataları yoxlayırıq
data.isnull().sum()

# Nümunə üçün 100 ədəd ev haqqında məlumatı nəzərdən keçirəcəyik
data = data.dropna(subset=['lat', 'long'])
data = data.sample(100, random_state=1)

# Qiymətlərin tipini integer tipinə çeviririk
data['price'] = data['price'].replace('[\$,]', '', regex=True).astype(int)

# 100 dollardan daha ucuz evləri seçirik
under_1000 = data[data['price'] < 1000]
count_under_1000 = under_1000.shape[0]

print(f"1000 dollardan ucuz evlərin sayı: {count_under_1000}")

# Bu verilənləri əks etdirən histogram hazırlayırıq
sns.histplot(under_1000['price'], bins=20)
plt.title('1000 dollardan ucuz evlərin qiymət bölgüsü')
plt.xlabel('Price ($)')
plt.ylabel('Count')
plt.show()

# Müəyyən məkan ətrafında mərkəzləşdirilmiş xəritə yaradırıq. Biz bu nümunədə Nyu Yorka baxacağıq.
map = folium.Map(location=[40.7128, -74.0060], zoom_start=12)

# For loopundan istifadə eədrək, xəritəyə işarələr əlavə edirik.
for index, row in data.iterrows():
    folium.Marker([row['lat'], row['long']], popup=f"Price: ${row['price']}").add_to(map)

# Nəticə:
map

map.save("airbnb_map.html")

low_price = data['price'].quantile(0.33)
high_price = data['price'].quantile(0.66)

# Bu bölgü üçün aşağıdakı funksiyanı yazmaq lazımdır
def price_category(price):
    if price <= low_price:
        return 'low'
    elif price <= high_price:
        return 'average'
    else:
        return 'high'

data['price_category'] = data['price'].apply(price_category)

# Bölgü üzrə işarələri rənglərlə fərqləndirmək üçün aşağıdakı kimi yazırıq
color_map = {
    'low': 'green',     # Aşağı qiymətli evlər
    'average': 'orange', # Orta qiymətli evlər
    'high': 'red'        # Yüksək qiymətli evlər
}

# Rəngləri for loopundan istifadə etməklə işarələrə mənimsədirik:
for index, row in data.iterrows():
    folium.Marker(
        [row['lat'], row['long']],
        popup=f"Price: ${row['price']}",
        icon=folium.Icon(color=color_map[row['price_category']])
    ).add_to(map)
 map

map.save("airbnb_map.html")

