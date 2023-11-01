# 라이브러리 불러오기
import matplotlib.pylab as plt
import seaborn as sns
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler  # 라이브러리 로딩
from sklearn.preprocessing import StandardScaler  # 라이브러리 로딩
from sklearn.preprocessing import LabelEncoder  # 라이브러리 로딩
from sklearn.preprocessing import OneHotEncoder  # 라이브러리 로딩
from sklearn.model_selection import train_test_split    # 라이브러리 로딩


# 실습 데이터 세트 로드 (펭귄 데이터)
penguins = sns.load_dataset("penguins")
penguins.head()

# 결측값 제거
penguins = penguins.dropna().reset_index(drop=True)

# 데이터 분포 확인
plt.figure(figsize=(15, 5))
sns.histplot(data=penguins)
plt.show()


scaler = MinMaxScaler() # 스케일러 정의

penguins_normed = penguins.copy()
features = penguins_normed[['bill_length_mm','bill_depth_mm','flipper_length_mm','body_mass_g']]    # 정규화 대상 컬럼
features_normed = scaler.fit_transform(features)    # 정규화 

# 정규화 된 데이터로 바꿔주기
penguins_normed = penguins_normed.assign(bill_length_mm = features_normed[:,0],
                                         bill_depth_mm = features_normed[:,1],
                                         flipper_length_mm = features_normed[:,2],
                                         body_mass_g = features_normed[:,3])

# 데이터 분포 확인
plt.figure(figsize=(15, 5))
sns.histplot(data=penguins_normed)
plt.show()


scaler = StandardScaler() # 스케일러 정의

penguins_scaled = penguins.copy()
features = penguins_scaled[['bill_length_mm','bill_depth_mm','flipper_length_mm','body_mass_g']]    # 표준화 대상 컬럼
features_stand = scaler.fit_transform(features)    # 표준화 

# 데이터 분포 확인
plt.figure(figsize=(15, 5))
sns.histplot(data=penguins_scaled)

encoder = LabelEncoder() # 인코더 정의

penguins_label = penguins_scaled.copy()
features = penguins_label[['species', 'island', 'sex']]    # 인코딩 대상 컬럼
encoded = features.apply(encoder.fit_transform)    # 인코딩 실행 

# 수치형 데이터로 바꿔주기
penguins_label = penguins_label.assign(species = encoded['species'],
                                           island = encoded['island'],
                                           sex = encoded['sex'])

encoder = OneHotEncoder() # 인코더 정의

penguins_onehot = penguins_scaled.copy()
features = penguins_onehot[['species', 'island', 'sex']]    # 인코딩 대상 컬럼
encoded = encoder.fit_transform(features).toarray()    # 인코딩 실행 

# 기존 범주형 컬럼 버리기
penguins_onehot = penguins_onehot.drop(columns=['species', 'island', 'sex'])

# 인코딩 결과 데이터 프레임 생성
encoded_df = pd.DataFrame(encoded)
encoded_df.columns = encoder.get_feature_names_out()

# 기존 데이터 프레임과 결합
penguins_onehot = pd.concat([penguins_onehot, encoded_df], axis=1)

X = penguins_label.drop('sex', axis=1)  # 예측에 사용할 변수 
Y = penguins_label['sex']  

# 학습 / 테스트 세트 분할
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, shuffle=True)

print(X_train)