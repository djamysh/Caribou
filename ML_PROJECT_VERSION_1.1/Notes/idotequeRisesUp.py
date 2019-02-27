import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy.random as npr
from sklearn.decomposition import PCA
import numpy as np

def get_column(data,columnIndex):
    data = data.T #Transpoze alınır
    return data[columnIndex]

activite1 = [
            [
                npr.randint(45,60), #İsteklilik
                npr.randint(30,40), #Yorgunluk
                npr.randint(75,90), #Moral
                npr.randint(75,95),  #Son Verim
                "OP1"
            ]
            for i in range(20)]
activite2 = [
        [
            npr.randint(15,20),
            npr.randint(35,45),
            npr.randint(45,60),
            npr.randint(50,70),
            "OP2"
        ]
        for i in range(20)]

activite3 = [
        [
            npr.randint(70,80),
            npr.randint(45,55),
            npr.randint(50,65),
            npr.randint(25,45),
            "OP3"
        ]
        for i in range(20)]

df = pd.DataFrame(activite1+activite2+activite3,columns = ["İsteklilik","Yorgunluk","Moral","Verim","Aktivite"])
dfX = df.iloc[:,:3]
dfY = df.iloc[:,3]

dcp = PCA(n_components=3)
dfXdcp = dcp.fit_transform(dfX)

df1Xdcp = dfXdcp[:20]
x1_maindcp = get_column(df1Xdcp,0)
y1_maindcp = get_column(df1Xdcp,1)
z1_maindcp = get_column(df1Xdcp,2)

df2Xdcp = dfXdcp[20:40]
x2_maindcp = get_column(df2Xdcp,0)
y2_maindcp = get_column(df2Xdcp,1)
z2_maindcp = get_column(df2Xdcp,2)

df3Xdcp = dfXdcp[40:]
x3_maindcp = get_column(df3Xdcp,0)
y3_maindcp = get_column(df3Xdcp,1)
z3_maindcp = get_column(df3Xdcp,2)




df1 = pd.DataFrame(activite1,columns = ["İsteklilik","Yorgunluk","Moral","Verim","Aktivite"])
op1X = df1.iloc[:,:3]
x1 = op1X.iloc[:,0]
y1 = op1X.iloc[:,1]
z1 = op1X.iloc[:,2]

dcp1 = PCA(n_components=3)
op1Xdcp = dcp1.fit_transform(op1X)
x1dcp = get_column(op1Xdcp,0)
y1dcp = get_column(op1Xdcp,1)
z1dcp = get_column(op1Xdcp,2)

op1Y = df1.iloc[:,3]

df2 = pd.DataFrame(activite2,columns = ["İsteklilik","Yorgunluk","Moral","Verim","Aktivite"])
op2X = df2.iloc[:,:3]
x2 = op2X.iloc[:,0]
y2 = op2X.iloc[:,1]
z2 = op2X.iloc[:,2]

dcp2 = PCA(n_components=3)
op2Xdcp = dcp2.fit_transform(op2X)
x2dcp = get_column(op2Xdcp,0)
y2dcp = get_column(op2Xdcp,1)
z2dcp = get_column(op2Xdcp,2)

op2Y = df2.iloc[:,3]

df3 = pd.DataFrame(activite3,columns = ["İsteklilik","Yorgunluk","Moral","Verim","Aktivite"])
op3X = df3.iloc[:,:3]
x3 = op3X.iloc[:,0]
y3 = op3X.iloc[:,1]
z3 = op3X.iloc[:,2]

dcp3 = PCA(n_components=3)
op3Xdcp = dcp3.fit_transform(op3X)
x3dcp = get_column(op3Xdcp,0)
y3dcp = get_column(op3Xdcp,1)
z3dcp = get_column(op3Xdcp,2)

op3Y = df3.iloc[:,3]

"""
fig1 = plt.figure()
ax = fig1.add_subplot(111, projection='3d')
ax.scatter(x1,y1,z1,label="Aktivite 1",color = "red",marker ="o")
ax.scatter(x2,y2,z2,label="Aktivite 2",color = "green",marker ="o")
ax.scatter(x3,y3,z3,label="Aktivite 3",color = "blue",marker ="o")
ax.set_xlabel("İsteklilik")
ax.set_ylabel("Yorgunluk")
ax.set_zlabel("Moral")
plt.title("Psudo Veri")
plt.legend()
plt.show()



fig2 = plt.figure()
ax = fig2.add_subplot(111, projection='3d')
ax.scatter(x1dcp,y1dcp,z1dcp,label="Aktivite 1",color = "red",marker ="o")
ax.scatter(x2dcp,y2dcp,z2dcp,label="Aktivite 2",color = "green",marker ="o")
ax.scatter(x3dcp,y3dcp,z3dcp,label="Aktivite 3",color = "blue",marker ="o")
ax.set_xlabel("İsteklilik")
ax.set_ylabel("Yorgunluk")
ax.set_zlabel("Moral")
plt.title("Psudo Veri Decomposited")
plt.legend()
plt.show()

fig3 = plt.figure()
ax = fig3.add_subplot(111, projection='3d')
ax.scatter(x1_maindcp,y1_maindcp,z1_maindcp,label="Aktivite 1",color = "red",marker ="o")
ax.scatter(x2_maindcp,y2_maindcp,z2_maindcp,label="Aktivite 2",color = "green",marker ="o")
ax.scatter(x3_maindcp,y3_maindcp,z3_maindcp,label="Aktivite 3",color = "blue",marker ="o")
ax.set_xlabel("İsteklilik")
ax.set_ylabel("Yorgunluk")
ax.set_zlabel("Moral")
plt.title("Psudo Veri Decomposited")
plt.legend()
plt.show()

"""

from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.cross_validation import train_test_split

data = df.iloc[:,:4].values
x_train,x_test,y_train,y_test = train_test_split(dfX,dfY,test_size = 0.33)

obj1 = KNeighborsRegressor(n_neighbors=3)
obj1.fit(x_train,y_train)
y_pred = obj1.predict(x_test)
r2s1 = r2_score(y_test,y_pred)
#print("1 - r2 : ",r2s1)
"""
dcpobj = PCA(n_components=4)
data_dcp = dcpobj.fit_transform(data)
X = data_dcp.T[:3].T
Y = data_dcp.T[3].T

x_train2,x_test2,y_train2,y_test2 = train_test_split(X,Y,test_size = 0.33)

obj2 = KNeighborsRegressor(n_neighbors=3)
obj2.fit(x_train2,y_train2)
y_pred = obj2.predict(x_test2)
r2s2 = r2_score(y_test2,y_pred)
print("2 - r2 : ",r2s2)

plt.bar(["Normal"],[r2s1],align='center')
plt.bar(["PCA"],[r2s2],align='center')
plt.plot([-2,2],[0,0],color = "black")
plt.plot([-1,-1],[-2,2],color = "black")
plt.grid(True)
plt.show()
"""
from sklearn.cluster import KMeans
from sklearn.metrics import r2_score
from sklearn.cross_validation import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV


import statsmodels.formula.api as sm
processData = dfX.iloc[:,[0,1,2]]
	
regressor_OLS = sm.OLS(endog = dfY.values, exog = processData).fit()
print(list(regressor_OLS.pvalues))
parameterList1 = [{}]
parameterList2 = [{"n_estimators":list(range(50,55))}]
parameterList3 = [{"metric":["euclidean","minkowski","chebyshev","manhattan"],"n_neighbors":list(range(1,5))}]


LinearRegressionSearcher = GridSearchCV(estimator=LinearRegression(),param_grid =parameterList1,scoring = 'r2',cv = 5)
LinearRegressionSearcher.fit(op1X,op1Y)
lrScore = LinearRegressionSearcher.best_score_
RandomForestRegressorSearcher = GridSearchCV(estimator=RandomForestRegressor(),param_grid =parameterList2,scoring = 'r2',cv = 5)
RandomForestRegressorSearcher.fit(op1X,op1Y)
rfScore = RandomForestRegressorSearcher.best_score_
KNeighborsRegressorSearcher = GridSearchCV(estimator=KNeighborsRegressor(),param_grid =parameterList3,scoring = 'r2',cv = 5)
KNeighborsRegressorSearcher.fit(op1X,op1Y)
knnScore = KNeighborsRegressorSearcher.best_score_

plt.bar(["Doğrusal Regresyon","Rastgele Orman","KNN"],[lrScore,rfScore,knnScore],width = 0.5,align = "center")
plt.title("Gerçek veri ile eğitilmiş algoritmaların R2 skorları")
plt.show()


