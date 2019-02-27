import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans
from sklearn.metrics import r2_score
from sklearn.cross_validation import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV


dataPath = "/home/wasptheslimy/Desktop/ML_Project_Version1.1/NotKodları/realData.csv"
data = pd.read_csv(dataPath)

data.drop(['index'],inplace = True,axis = 1)


X = data.iloc[:,:3]
Y = data.iloc[:,3]


from sklearn.ensemble import RandomForestRegressor

paramsRandomForestRegressor = [{"n_estimators":list(range(5,20))}]
RandomForestRegressorSearcher = GridSearchCV(estimator=RandomForestRegressor(),param_grid =paramsRandomForestRegressor,scoring = 'r2',cv = 5)
RandomForestRegressorSearcher.fit(X,Y)
RFScore = RandomForestRegressorSearcher.best_score_
print("Random Forest Regressor Score :",RFScore)



from sklearn.neighbors import KNeighborsRegressor

paramsKNeighborsRegressor = [{"metric":["euclidean","minkowski","chebyshev","manhattan"],"n_neighbors":list(range(1,5))}]
KNeighborsRegressorSearcher = GridSearchCV(estimator=KNeighborsRegressor(),param_grid =paramsKNeighborsRegressor,scoring = 'r2',cv = 5)
KNeighborsRegressorSearcher.fit(X,Y)
KNeighborsRegressorScore = KNeighborsRegressorSearcher.best_score_
print("KNN Score :",KNeighborsRegressorScore)


paramsLinearRegression = [{}]
LinearRegressionSearcher = GridSearchCV(estimator=LinearRegression(),param_grid =paramsLinearRegression,scoring = 'r2',cv = 5)
LinearRegressionSearcher.fit(X,Y)
LinearRegressionScore = LinearRegressionSearcher.best_score_
print("Linear Regression Regressor Score :",LinearRegressionScore)


plt.bar(["Linear Regression"],height = LinearRegressionScore,align = "center",label = "Doğrusal Regresyon")
plt.bar(["KNN"],height =KNeighborsRegressorScore,align = "center",label = "K-En Yakın Komşu Regresyonu")
plt.bar(["Random Forest"],height = RFScore,align = "center",label = "Rastgele Orman")
plt.title("Zorlayıcı veri karşısında algoritma başarıları")
plt.ylim(-0.25,1)
plt.xlim(-1/2,5/2)
plt.xlabel("Algoritmalar")
plt.ylabel("Skor")
plt.grid(True)
plt.legend()
plt.show()



yLabeled = list()
for i in Y:
    if i <= 25:
        yLabeled.append("l")#low

    elif i>25 and i<=50:
        yLabeled.append("m1")#medium1
    
    elif i>50 and i<=75:
        yLabeled.append("m2")#medium1
    
    elif i>75 and i<=100:
        yLabeled.append("h")

dfY = pd.DataFrame(np.array(yLabeled).reshape(len(yLabeled),1),columns=["Verim"])
Y2 = list()
for i in Y:
    if i<=50:
        Y2.append(0)
    
    elif i>50 and i<=100:
        Y2.append(1)
dfY2 = pd.DataFrame(np.array(Y2).reshape(len(Y2),1),columns=["Verim"])

isteklilik = data[["isteklilik"]].values
yorgunluk = data[["yorgunluk"]].values
moral = data[["moral"]].values


istN = list()
for d in isteklilik:
    if d < 50:
        istN.append(np.float(0))
    else:
        istN.append(np.float(1))

yorgN = list()
for d in yorgunluk:
    if d < 33:
        yorgN.append("yorgun")
    elif d>= 33 and d <66:
        yorgN.append("normal")
    else:
        yorgN.append("dinç")

moralN = list()
for d in moral:
    if d < 25:
        moralN.append("l")
    elif d>= 25 and d <50:
        moralN.append("m")
    elif d>= 50 and d <75:
        moralN.append("n")
    else:
        moralN.append("h")

dfisteklilik = pd.DataFrame(np.array(istN).reshape(len(istN),1),columns = ["isteklilik"])# 0 > isteksiz ; 1 > istekli
dfyorgunluk = pd.DataFrame(yorgN,columns = ["yorgunluk"])
dfmoral = pd.DataFrame(moralN,columns = ["moral"])
weirdX = pd.concat([dfisteklilik,dfyorgunluk,dfmoral],axis = 1)

#####################################################################
from sklearn.preprocessing import OneHotEncoder,LabelEncoder
#####################################################################


le1 = LabelEncoder()
ohe1 = OneHotEncoder(categorical_features="all")

labelEncodedYorgunluk = le1.fit_transform(dfyorgunluk)# Label Encoding
labelEncodedYorgunluk = labelEncodedYorgunluk.reshape(len(labelEncodedYorgunluk),1)
columnsYorgunluk = le1.classes_
catYorgunluk = ohe1.fit_transform(labelEncodedYorgunluk).toarray()#One Hot Encoding 
dfyorgunluk = pd.DataFrame(catYorgunluk,columns = columnsYorgunluk)
dfyorgunluk = dfyorgunluk.iloc[:,:-1]#Son kolon çıkarılarak dummy variable'dan kurtarılır.

#####################################################################
#####################################################################


le2 = LabelEncoder()
ohe2 = OneHotEncoder(categorical_features="all")

labelEncodedMoral = le2.fit_transform(dfmoral)# Label Encoding
labelEncodedMoral = labelEncodedMoral.reshape(len(labelEncodedMoral),1)
columnsMoral = le2.classes_
catMoral = ohe2.fit_transform(labelEncodedMoral).toarray()#One Hot Encoding 
dfmoral = pd.DataFrame(catMoral,columns=columnsMoral)

dfmoral = dfmoral.iloc[:,:-1]#Son kolon çıkarılarak dummy variable'dan kurtarılır.


dataset = pd.concat([dfisteklilik,dfyorgunluk,dfmoral,dfY],axis=1)
X_adjusted = pd.concat([dfisteklilik,dfyorgunluk,dfmoral],axis=1)
Y_adjusted = dfY



from xgboost import XGBClassifier
from sklearn.neighbors import KNeighborsClassifier

parameterList3 = [{"metric":["euclidean","minkowski","chebyshev","manhattan"],"n_neighbors":list(range(1,5))}]
searcher1 = GridSearchCV(estimator=KNeighborsClassifier(),param_grid =parameterList3,scoring = 'accuracy',cv = 5)
searcher1.fit(X_adjusted,dfY2.values.reshape(len(dfY2.index)))
print("Accuracy KNN (GridSearchCV; cv = 5) : ",searcher1.best_score_)


parameterList4 = [{"booster":["gbtree","gblinear"],
                    "eta":np.arange(1,2)*0.1,
                    "n_estimators":np.arange(5,10),
                    "max_depth":np.arange(3,10,2),
                    "min_child_weight":np.arange(1,6,2)}]

searcher2 = GridSearchCV(estimator=XGBClassifier(objective = "binary:logistic"),param_grid =parameterList4,scoring = 'accuracy',cv = 5)
searcher2.fit(X_adjusted,dfY2.values.reshape(len(dfY2.index)))
print("Accuracy XGBoost(GridSearchCV; cv = 5) : ",searcher2.best_score_)

from sklearn.naive_bayes import GaussianNB
searcher3 = GridSearchCV(estimator=GaussianNB(),param_grid =[{}],scoring = 'accuracy',cv = 5)
searcher3.fit(X_adjusted,dfY2.values.reshape(len(dfY2.index)))
print("Accuracy Gaussian Naive Bayes(GridSearchCV; cv = 5) : ",searcher3.best_score_)

import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import cross_val_score

###############################Deep Learning 1


def neural_network_1():
    classifier = Sequential()
    classifier.add(Dense(6,activation="relu",init = "uniform",input_dim = 6))
    classifier.add(Dense(6,activation="relu",init = "uniform"))
    classifier.add(Dense(1,activation="sigmoid",init = "uniform"))

    classifier.compile(optimizer="rmsprop",loss ="binary_crossentropy",metrics=["accuracy"])    

    return classifier

def neural_network_2():
        # Start neural network
    print("network")
    network = Sequential()

    # Add fully connected layer with a ReLU activation function
    network.add(Dense(units=6, activation='relu', input_shape=(6,)))

    # Add fully connected layer with a ReLU activation function
    network.add(Dense(units=6, activation='relu'))

    # Add fully connected layer with a sigmoid activation function
    network.add(Dense(units=1, activation='sigmoid'))

    # Compile neural network
    network.compile(loss='binary_crossentropy', # Cross-entropy
                    optimizer='rmsprop', # Root Mean Square Propagation
                    metrics=['accuracy']) # Accuracy performance metric
    
    # Return compiled network
    return network

neural_networkA = KerasClassifier(build_fn=neural_network_1, 
                                epochs=50, 
                                batch_size=100, 
                                verbose=1)

dl1Score = cross_val_score(neural_networkA,X = X_adjusted,y = dfY2,cv=5).mean()
meanedDl1Score = np.array(dl1Score).mean()
print("K-Fold used mean based DL1 score :",meanedDl1Score)


from sklearn.neighbors import RadiusNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
paramGridLogisticRegression = param_grid = [{'C': [0.001, 0.01, 0.1,.5, 1,1.5,2,2.5,3,3.5,4,4.5,5,10, 100, 1000] }]
searcherLogistic = GridSearchCV(estimator=LogisticRegression(penalty="l2"),param_grid =paramGridLogisticRegression,scoring = 'accuracy',cv = 5)
searcherLogistic.fit(X_adjusted,dfY2)
print("Logistic Regression Score GridSearchCV(cv = 5) :" ,searcherLogistic.best_score_)


paramsRandomForestRegressor = [{"n_estimators":list(range(3,20)),"criterion":["entropy","gini"]}]
searcherRandomForest = GridSearchCV(estimator=RandomForestClassifier(),param_grid =paramsRandomForestRegressor,scoring = 'accuracy',cv = 5)
searcherRandomForest.fit(X_adjusted,dfY2)
print("Random Forest Regression Score GridSearchCV(cv = 5) :" ,searcherRandomForest.best_score_)



plt.bar(x = ["ANN"],height=dl1Score,align = "center",label = "Yapay Sinir Ağı")
plt.bar(x = ["XGBoost"],height = searcher2.best_score_,align = "center",label = "Extra Gradient Boosting")
plt.bar(x = ["KNN"],height = searcher1.best_score_,align = "center",label = "K-En Yakın Komşu")
plt.bar(x = ["GaussianNB"],height = searcher3.best_score_,align = "center",label = "Gaussian Naive Bayes")
plt.bar(x = ["Logistic"],height = searcherLogistic.best_score_,align = "center",label = "Logistic Regresyon")
plt.bar(x = ["Random Forest"],height = searcherRandomForest.best_score_,align = "center",label = "Rastgele Orman")

plt.title("Zorlayıcı veri karşısında algoritma başarıları")
plt.ylim(0,1.01)
plt.grid(True)
plt.legend()
plt.show()


