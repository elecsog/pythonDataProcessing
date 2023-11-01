# 라이브러리 불러오기
import matplotlib.pylab as plt
import seaborn as sns
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler  # 라이브러리 로딩
from sklearn.preprocessing import LabelEncoder  # 라이브러리 로딩
from sklearn.model_selection import train_test_split    # 라이브러리 로딩
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# 실습 데이터 세트 로드 (펭귄 데이터)
penguins = sns.load_dataset("penguins")

# 결측값 제거
penguins = penguins.dropna().reset_index(drop=True)
scaler = MinMaxScaler() # 스케일러 정의

features = penguins[['bill_length_mm','bill_depth_mm','flipper_length_mm','body_mass_g']]    # 정규화 대상 컬럼
features_normed = scaler.fit_transform(features)    # 정규화 

# 정규화 된 데이터로 바꿔주기
penguins = penguins.assign(bill_length_mm = features_normed[:,0],
                            bill_depth_mm = features_normed[:,1],
                            flipper_length_mm = features_normed[:,2],
                            body_mass_g = features_normed[:,3])

encoder = LabelEncoder() # 인코더 정의

features = penguins[['species', 'island', 'sex']]    # 인코딩 대상 컬럼
encoded = features.apply(encoder.fit_transform)    # 인코딩 실행 

# 수치형 데이터로 바꿔주기
penguins = penguins.assign(species = encoded['species'],
                            island = encoded['island'],
                            sex = encoded['sex'])

X = penguins.drop('sex', axis=1)  # 예측에 사용할 변수 
Y = penguins['sex']               # 예측할 변수

# 학습 / 테스트 세트 분할
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, shuffle=True)

lr_model = LogisticRegression(verbose=2)

lr_model.fit(X_train, Y_train)

# 수컷(Male) : 1, 암컷(Female) : 0
predictions = lr_model.predict(X_test)

knc_acc = accuracy_score(Y_test, predictions)
print('KNeighborsClassifier 모델의 예측 정확도는 {}% 입니다.'.format(round(knc_acc*100)))