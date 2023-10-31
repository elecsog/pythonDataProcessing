# 라이브러리 임포트
import requests
import pandas as pd

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
