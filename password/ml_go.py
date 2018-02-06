import numpy
import scipy
import sklearn
from  sklearn.neighbors import KNeighborsClassifier #KNN分类模型

x_train=[[185,80,43],[170,70,41],[163,45,36],[165,55,39],[156,41,35]]  #身高 体重 鞋码
y_train=["男人","男人","女人","男人","女人"]

#机器学习并训练数据，自己建立模型预测

knn=KNeighborsClassifier(2)  #两个父类
knn.fit(x_train,y_train) #训练机器，用已有数据
print(knn.predict([[165,46,38],[175,73,40],[172,42,37]]))
