#####################################
#Preprocessing
import pandas as pd
import numpy as np
#####################################
#Regressions
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
#####################################
#Clasifications
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
#####################################
#Model Selection
from sklearn.model_selection import GridSearchCV





class ML():
    def __init__(self,data_dict,*args, **kwargs):
        self.data_dict = data_dict
        
        
        self.predictable_data_dict = self.findPredictableFrames()
        if self.predictable_data_dict != dict():
            self.generalClassificationDataset = self.generalSituationsDataset

            self.algorithmDict = self.findBestRegression

            self.classificationEstimator = self.findBestClassification
        
    def findPredictableFrames(self):
        predictable_data_dict = dict()
        for key in self.data_dict:
            if key != "SleepTable":
                if len(self.data_dict[key].index) < 15:
                    pass
                else:
                    if ("Date" and "TimeRange") in list(self.data_dict[key].columns):
                        self.data_dict[key] = self.data_dict[key].drop(["Date","TimeRange"],axis = 1)#Görecelik
                    predictable_data_dict[key] = self.data_dict[key]
        return predictable_data_dict

    def bestRegression(self,specifiedDataFrame):
        X = specifiedDataFrame.iloc[:,:-1]
        Y = np.ravel(specifiedDataFrame.iloc[:,-1:].values)
        
        
        modelResults = list()

        res1 = self.LinRegConclusion(X,Y)

        res2 = self.KNNConclusion(X,Y)

        res3 = self.RandomForestConclusion(X,Y)


        modelResults.append(res1)
        modelResults.append(res2)
        modelResults.append(res3)

        return max(modelResults,key = lambda tup:tup[0])
    
    def LinRegConclusion(self,X,Y):
        paramsLinearRegression = [{}]
        LinearRegressionSearcher = GridSearchCV(estimator=LinearRegression(),param_grid =paramsLinearRegression,scoring = 'r2',cv = 5)
        LinearRegressionSearcher.fit(X,Y)
        LinearRegressionScore = LinearRegressionSearcher.best_score_
        LinearRegressionestimator = LinearRegressionSearcher.best_estimator_

        return (LinearRegressionScore,LinearRegressionestimator)

    def RandomForestConclusion(self,X,Y):
        paramsRandomForestRegressor = [{"n_estimators":list(range(5,20))}]
        RandomForestRegressorSearcher = GridSearchCV(estimator=RandomForestRegressor(),param_grid =paramsRandomForestRegressor,scoring = 'r2',cv = 5)
        RandomForestRegressorSearcher.fit(X,Y)
        RandomForestRegressorScore = RandomForestRegressorSearcher.best_score_
        RandomForestRegressorestimator = RandomForestRegressorSearcher.best_estimator_

        return (RandomForestRegressorScore,RandomForestRegressorestimator)

    def KNNConclusion(self,X,Y):
        paramsKNeighborsRegressor = [{"metric":["euclidean","minkowski","chebyshev","manhattan"],"n_neighbors":list(range(1,5))}]
        KNeighborsRegressorSearcher = GridSearchCV(estimator=KNeighborsRegressor(),param_grid =paramsKNeighborsRegressor,scoring = 'r2',cv = 5)
        KNeighborsRegressorSearcher.fit(X,Y)
        KNeighborsRegressorScore = KNeighborsRegressorSearcher.best_score_
        KNeighborsRegressorestimator = KNeighborsRegressorSearcher.best_estimator_

        return (KNeighborsRegressorScore,KNeighborsRegressorestimator)

    def giveMeAdvice(self,data):

        results = list()
        for key in self.algorithmDict:
            obj = self.algorithmDict[key][1]
            efficiency = obj.predict(data)

            results.append((efficiency,key))

        adviceList = sorted(results,key = lambda tup:tup[0],reverse = True)
        return adviceList 


    @property
    def findBestRegression(self):
        self.algorithmDict = dict()
        for key in self.predictable_data_dict:
            algorthm = self.bestRegression(self.predictable_data_dict[key])
            self.algorithmDict[key] = algorthm
        
        return self.algorithmDict
            
    @property
    def generalSituationsDataset(self):

        generalDF = pd.DataFrame()
        for key in self.predictable_data_dict:
            df = self.predictable_data_dict[key]
            job = key
            
            y = [job for i in range(len(df.index))]
            y = pd.DataFrame(y)


            newDf = pd.concat([df,y],axis = 1) # axis = 1 ==> X-axis ; axis = 0 ==> Y-axis
            
            generalDF = pd.concat([generalDF,newDf],axis = 0)
        
        generalDF.columns = list(df.columns)+["Job"]
        generalDF.index = range(len(generalDF.index))

        generalDF.drop("Efficiency",axis = 1,inplace = True)#Göreceli bir durum.Genelleştir..
        return generalDF

    @property
    def findBestClassification(self):
        X = self.generalClassificationDataset.iloc[:,:-1]
        Y = np.ravel(self.generalClassificationDataset.iloc[:,-1:].values)

        res1 = self.GaussianNBConclusion(X,Y)
        res2 = self.KNNClasficationConclusion(X,Y)

        bestClassification = max([res1,res2],key = lambda tup:tup[0])
        classificationEstimator = bestClassification[1]
        return classificationEstimator

    def GaussianNBConclusion(self,X,Y):
        paramsGaussianNB = [{}]
        GaussianNBSearcher = GridSearchCV(estimator=KNeighborsClassifier(),param_grid =paramsGaussianNB,scoring = 'accuracy',cv = 5)
        GaussianNBSearcher.fit(X,Y)
        GaussianNBScore = GaussianNBSearcher.best_score_
        GaussianNBestimator = GaussianNBSearcher.best_estimator_

        return (GaussianNBScore,GaussianNBestimator)

    def KNNClasficationConclusion(self,X,Y):
        paramsKNeighborsClassification = [{"metric":["euclidean","minkowski","chebyshev","manhattan"],"n_neighbors":list(range(1,5))}]
        KNeighborsClassificationSearcher = GridSearchCV(estimator=KNeighborsClassifier(),param_grid =paramsKNeighborsClassification,scoring = 'accuracy',cv = 5)
        KNeighborsClassificationSearcher.fit(X,Y)
        KNeighborsClassificationScore = KNeighborsClassificationSearcher.best_score_
        KNeighborsClassificationestimator = KNeighborsClassificationSearcher.best_estimator_

        return (KNeighborsClassificationScore,KNeighborsClassificationestimator)

    def GiveGeneralActivity(self,data):

        activity = self.classificationEstimator.predict(data)

        return activity