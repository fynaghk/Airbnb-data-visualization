import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
