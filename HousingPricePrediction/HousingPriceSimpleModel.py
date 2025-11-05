# 01.Library for dataset processing
import pandas as pd
import numpy as np
# 02. Library for train model
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
# 03. Library for evaluation model
from sklearn import metrics
# 04. Library for saving model
import pickle
from sklearn import metrics


#use pandas to read CSV dataset
df = pd.read_csv('dataset/USA_Housing.csv')
#call functions about get dataset information:
print(df.head())
print(df.info())


#set X matrix
#df.columns[:5] meaning:
#['Avg. Area Income', 'Avg. Area House Age', 'Avg. Area Number of Rooms',
# 'Avg. Area Number of Bedrooms', 'Area Population']
X = df[['Avg. Area Income', 'Avg. Area House Age', 'Avg. Area Number of Rooms','Avg. Area Number of Bedrooms', 'Area Population']]
y = df['Price']
# Printing for observation:
print(X)
print(y)

#chia dữ liệu để train:
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=101)

lm = LinearRegression()

lm.fit(X_train, y_train)

print("Input 1:")
print([X_test.iloc[0]])

pre1 = lm.predict([X_test.iloc[0]])
print("Housing Price prediction 1 =", pre1)

print("Input 2:")
input2=[66774.995817, 5.717143, 7.795215, 4.320000, 36788.980327]
pre2 = lm.predict([input2])
print("Housing Price prediction 2 =", pre2)
#đánh giá mô hình dự đoán:
print(lm.intercept_)
coeff_df = pd.DataFrame(lm.coef_,X.columns,columns=['Coefficient'])
print(coeff_df)

#chỉ số đánh giá:
predictions = lm.predict(X_test)
print("Full Housing Price Predictions:")
print(predictions)
print('MAE:', metrics.mean_absolute_error(y_test, predictions))
print('MSE:', metrics.mean_squared_error(y_test, predictions))
print('RMSE:', np.sqrt(metrics.mean_squared_error(y_test, predictions)))

#kết xuất mô hinh máy học ra ổ cứng (file zip)
modelname = "housingmodel.zip"

pickle.dump(lm, open(modelname, 'wb'))