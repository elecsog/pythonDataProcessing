# 라이브러리 임포트
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import matplotlib.font_manager as fm
import matplotlib as mpl 
import numpy as np
import seaborn as sns

# 실습 파일 로딩 (펭귄, 타이타닉)
df1 = sns.load_dataset("penguins")
df1 = df1[['species', 'island', 'bill_length_mm', 'bill_depth_mm', 'flipper_length_mm']]
df1 = df1.dropna().reset_index(drop=True)
df2 = sns.load_dataset("titanic")

df1.plot(kind='line', figsize=(15,5), title='penguine line graph')
plt.show()

df1.plot(kind='hist', figsize=(15,5), title = 'hitogram')
plt.show()

df1.plot(kind='box', figsize=(15,5), title = 'range')
plt.show()

pie_df = df2['pclass'].value_counts()
pie_df.plot(kind='pie', figsize=(15,8), title = 'ratio')
plt.show()

pie_df.plot(kind='pie', figsize=(15,8), title = 'ratio', autopct='%.1f%%', fontsize=20)
plt.show()

# 나이에 따른 타이타닉 승선 요금 시각화
df2.plot(kind='scatter', figsize=(15,8) , x='age', y='fare', title='price by age')
plt.show()

# 버블차트 (선실 정보 추가)
df2.plot(kind='scatter', figsize=(15,8) , x='age', y='fare', title='나이에 따른 타이타닉 승선 요금', s=df2['pclass']*100)
plt.show()
