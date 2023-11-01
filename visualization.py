# 라이브러리 임포트
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import matplotlib.font_manager as fm
import matplotlib as mpl 
import numpy as np
import requests

# 코드를 입력해 주세요
import requests
site1 = 'https://dbkpop.com/db/all-k-pop-idols'  # K-pop 아이돌 전체 정보
site2 = 'https://dbkpop.com/db/k-pop-girlgroups' # K-pop 여자 그룹 정보
site3 = 'https://dbkpop.com/db/k-pop-boybands'   # K-pop 남자 그룹 정보

r1 = requests.get(site1)
r2 = requests.get(site2)
r3 = requests.get(site3)

all_df = pd.read_html(r1.text, displayed_only=False)[0]
all_df.columns = all_df.columns.get_level_values(0)

girl_df = pd.read_html(r2.text, displayed_only=False)[0]
girl_df.columns = girl_df.columns.get_level_values(0)

boy_df = pd.read_html(r3.text, displayed_only=False)[0]
boy_df.columns = boy_df.columns.get_level_values(0)

print(all_df.head())
print(girl_df.head())
print(boy_df.head())

# 사용할 컬럼
all_cols = ['K. Stage Name', 'Date of Birth', 'Group', 'Country', 'Height', 'Gender']
girl_cols = ['Name', 'Short', 'Korean Name', 'Debut', 'Company', 'Members', 'Orig. Memb.', 'Active']
boy_cols = ['Name', 'Short', 'Korean Name', 'Debut', 'Company', 'Members', 'Orig. Memb.', 'Active']

# 컬럼 필터링
all_df = all_df[all_cols]
girl_df = girl_df[girl_cols]
boy_df = boy_df[boy_cols]

# 결측 값 치환
girl_df['Name'] = girl_df['Name'].fillna('_')
girl_df['Short'] = girl_df['Short'].fillna('_')

# 공통 컬럼(Group) 생성
girl_df['Group'] = girl_df['Name'] + '|' + girl_df['Short']
# 공통된 문자열을 키(컬럼)값으로 사용하기 위한 과정
for group_name in all_df['Group']:      # 전체 아이돌 데이터 프레임의 키(컬럼) 값 돌기
    if not pd.isna(group_name):         # 결측값이 아닌 경우에만 아래 과정 수행
        girl_df.loc[girl_df['Group'].str.contains(group_name), 'Group'] = group_name   # 겹치는 문자열로 대체

## boy_df 에도 적용

# 결측 값 치환
boy_df['Name'] = boy_df['Name'].fillna('_')
boy_df['Short'] = boy_df['Short'].fillna('_')

# 공통 컬럼(Group) 생성
boy_df['Group'] = boy_df['Name'] + '|' + boy_df['Short']

# 공통된 문자열을 키(컬럼)값으로 사용하기 위한 과정
for group_name in all_df['Group']:      # 전체 아이돌 데이터 프레임의 키(컬럼) 값 돌기
    if not pd.isna(group_name):         # 결측값이 아닌 경우에만 아래 과정 수행
        boy_df.loc[boy_df['Group'].str.contains(group_name), 'Group'] = group_name   # 겹치는 문자열로 대체


# 여자 아이돌 정보 합치기
df1 = pd.merge(all_df, girl_df, how='inner', on='Group')

# 남자 아이돌 정보 합치기
df2 = pd.merge(all_df, boy_df, how='inner', on='Group')
# 행 방향 (axis=0) 데이터 결합
df = pd.concat([df1, df2], axis=0)

df = df.reset_index(drop=True)

df = df.drop(columns = ['Name', 'Short'])

# 0값을 NaN 형으로 변환
df = df.replace(0, np.NaN)

# 결측값 개수 확인
# 이름이 결측인 경우 - 행 전체 제거
# 키가 결측인 경우 - 평균값 대체
# 데뷰일이 결측인 경우 - 행 전체 제거
df.isnull().sum()

# 이름, 데뷰일이 결측인 경우 - 행 전체 제거
df = df.dropna(subset=['K. Stage Name', 'Debut'])
# 키가 결측인 경우 - 평균값 대체
mean_value = df['Height'].mean()
df['Height'] = df['Height'].fillna(mean_value)

# 중복된 행 찾기
df[df.duplicated()]

# 아이돌 그룹 당 첫번째 행만 남기기
group_df = df.drop_duplicates(subset=['Group'], keep='first').reset_index(drop=True)

print(group_df)
# 성별 아이돌 그룹 비율
gender_df = group_df['Gender'].value_counts()
gender_df.plot(kind='pie', figsize=(15,8), title = 'gender ratio', autopct='%.1f%%', fontsize=20)
plt.show()