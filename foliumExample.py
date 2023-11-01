# 라이브러리 불러오기
import folium
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib as mpl 
import seaborn as sns

import requests
import json

import warnings
warnings.filterwarnings("ignore")

plt.rcParams['font.family'] ='Malgun Gothic'

# Map 함수를 이용해 지도를 focusing 합니다.
#folium.Map(location=[37.50327278745055, 127.04160945554442], zoom_start=18).show_in_browser()

'''
m = folium.Map(location=[37.50327278745055, 127.04160945554442], zoom_start=18)
#m.save('myfolium.html') 
marker = folium.Marker([37.50327278745055, 127.04160945554442],
                       popup = '패스트 캠퍼스',     # 마커 이름 입력
                       icon = folium.Icon(color='blue'))
marker.add_to(m)

# 원 형태 마커 표시
marker = folium.CircleMarker([37.50327278745055, 127.04160945554442],
                             radius = 100,    # 범위
                             color = 'skyblue',
                             fill_color = 'skyblue',
                             popup = '패스트 캠퍼스',     # 마커 이름 입력
                             icon = folium.Icon(color='blue'))
marker.add_to(m)
m.show_in_browser()
'''

# 상권 분석
# 실습 데이터 로딩
df = pd.read_csv('소상공인시장진흥공단_상가(상권)정보_서울.csv')

print(df.head())

# 필요한 컬럼만 필터링
df = df[['상호명', '상권업종소분류명', '시군구명', '위도', '경도']]
print(df['상권업종소분류명'].unique())

# 카페 데이터 필터링
coffee_df = df.loc[df['상권업종소분류명']=='커피전문점/카페/다방'].reset_index(drop=True)
print(coffee_df)

# 서울시 카페 브랜드 수 (상위 20개)
plt.figure(figsize=(15,10))
coffee_df['상호명'].value_counts()[:20].sort_values().plot(kind='barh')
plt.show()

# 상위 3개 브랜드 지역
top3_coffee = coffee_df.loc[coffee_df['상호명'].isin(['이디야커피', '스타벅스', '투썸플레이스'])]

# 시군구 그룹핑
top3_coffee_group = pd.DataFrame(top3_coffee.groupby(['시군구명','상호명'])['상호명'].count().reset_index(name ='매장수'))
print(top3_coffee_group)

# Seaborn 시각화
plt.figure(figsize=(20,10))
sns.barplot(data=top3_coffee_group, x='시군구명', y='매장수', hue ='상호명')
plt.show()

# 상위 3개 브랜드 지역
top3_coffee = coffee_df.loc[coffee_df['상호명'].isin(['이디야커피', '스타벅스', '투썸플레이스'])]

# 지도 중심점 잡기
mean_lat = top3_coffee['위도'].mean()
mean_lon = top3_coffee['경도'].mean()
m = folium.Map(location=[mean_lat, mean_lon], zoom_start=11)

# 맵 크기 조절
f = folium.Figure(width=1000, height=500)
m.add_to(f)

# 서울시 행정구역 GeoJSON 파일 로딩
soul_geo = 'https://raw.githubusercontent.com/southkorea/seoul-maps/master/kostat/2013/json/seoul_municipalities_geo_simple.json'
r = requests.get(soul_geo)
seoul_json = json.loads(r.content)
print(seoul_json)

# 지도에 지역구 구분 표시
m.choropleth(geo_data = seoul_json, fill_color = 'gray')

# 스타벅스용 맵 생성
sb_map = folium.Map(location=[mean_lat, mean_lon], zoom_start=11)
f = folium.Figure(width=1000, height=500)
sb_map = sb_map.add_to(f)

# 지역구 구분 색상 표시
starbucks_count = top3_coffee_group.loc[top3_coffee_group['상호명']=='스타벅스']
sb_map.choropleth(geo_data = seoul_json,
                    data = starbucks_count,
                    columns = ['시군구명', '매장수'],
                    fill_color = 'YlGn',
                    color='gray',
                    key_on = 'properties.name',
                    fill_opacity=0.5,
                    line_opacity=0.5,
                    legend_name = '지역구 별 스타벅스 매장 수')

# 지역구 구분 마커 표시
starbucks = top3_coffee_group.loc[top3_coffee_group['상호명']=='스타벅스']
starbucks_coord = top3_coffee.loc[top3_coffee['상호명']=='스타벅스']

for idx, row in starbucks_coord.iterrows():
    folium.Marker([row['위도'], row['경도']],
                  popup = '스타벅스',     # 마커 이름 입력
                  icon = folium.Icon(color='green')                  
                  ).add_to(sb_map)

sb_map.show_in_browser()
