# 라이브러리 임포트
import requests
import pandas as pd
import numpy as np


'''  // 슬라이싱 및 data 처리
site = 'https://dbkpop.com/db/all-k-pop-idols'
r = requests.get(site)

df = pd.read_html(r.text)[0]
df.columns = df.columns.get_level_values(0)
print(df.head())

print(df.info())

df = pd.read_csv('https://bit.ly/3gRXTfD')
df = df.iloc[:,1:11].head(10)
print(df)

print(df.loc[df['Korean Name']=='임윤아', ['Height']])

group_name = ['SNSD'] # 리스트 지정
df['Group'].isin(group_name)
print(df.loc[df['Group'].isin(group_name)])

new_row = {'Stage Name': 'FastCampus', 
           'Full Name': 'Fast Campus', 
           'Korean Name' : '패스트캠퍼스', 
           'K. Stage Name' : '패캠', 
           'Date of Birth' : '2017-01-01',
           'Group' : 'FC',
           'Country' : 'Soutch Korea',
           'Second Country' : None,
           'Height' : 180,
           'Weight' : 80}
'''
''' 정렬 '''
'''
df = pd.read_csv('https://bit.ly/3gRXTfD')
df = df.iloc[:,1:11].head(8)

df.info()

df.describe()

df.sort_index()

# 내림차순 정렬 (ascending=False 추가)
df.sort_index(ascending=False)

print(df.sort_values(by='Height'))

'''
'''
df = pd.read_csv('https://bit.ly/3gRXTfD')
df = df.iloc[:,1:11].head(200)
df = df.loc[(df['Height']!=0)&(df['Weight']!=0)].dropna(subset=['Group'], axis=0).reset_index(drop=True)
# index = '행 인덱스', columns = '열 인덱스', values = '조회하고 싶은 값', aggfunc = '집계방식(기본값은 평균)'
print(pd.pivot_table(df, index='Group', columns='Country', values='Height', aggfunc='mean'))
# index = '행 인덱스', columns = '열 인덱스', values = '조회하고 싶은 값', aggfunc = '집계방식(기본값은 평균)'
print(pd.pivot_table(df, index='Group', columns='Country', values='Height', aggfunc='sum'))
'''
'''
df = pd.read_csv('https://bit.ly/3gRXTfD')
df1 = df.iloc[:,1:11].head(5)
df2 = df.loc[3:10, ['Korean Name', 'Instagram']]

dfresult=  df1.join(df2.set_index('Korean Name'), on='Korean Name', how='left')
print(dfresult)

dfouter = pd.merge(df1, df2, on='Korean Name', how='outer')
print(dfouter)

'''
df = pd.read_csv('https://bit.ly/3gRXTfD')
df = df.iloc[15:30]
df = df[['K. Stage Name', 'Date of Birth', 'Group', 'Height', 'Weight', 'Birthplace']]
print(df)

# 0값을 NaN 형으로 변환
df = df.replace(0, np.NaN)
print(df)

# 결측 데이터 확인(isnull(), notnull())
df.isnull()
print(df.isnull())
print(df.isnull().sum())

# 기본적으로 결측인 값이 존재하면 행 모두 삭제합니다,
print(df.dropna())

# subset=['컬럼명'] 옵션을 지정하면 해당 컬럼만 검사합니다.
print(df.dropna(subset=['Group']))

# subset=['컬럼명'] 옵션을 지정하면 해당 컬럼만 검사합니다

# 평균 값으로 대체
mean_value = df['Weight'].mean()
df['Weight'] = df['Weight'].fillna(mean_value)
print(df)

df['Birthplace'] = df['Birthplace'].fillna(df['Birthplace'].value_counts().index[0])
print(df)

#