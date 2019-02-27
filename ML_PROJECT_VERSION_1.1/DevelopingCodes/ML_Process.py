#####################################
#Preprocessing
import pandas as pd
import numpy as np
#####################################
#Regressions
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression,LogisticRegression
from sklearn.ensemble import RandomForestRegressor
#####################################
#Clasifications
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
#####################################
#Dimension Reduction
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
#####################################
#Model Selection
from sklearn.model_selection import GridSearchCV
#####################################
#Progression Vis.
from PyQt5.QtCore import QTimer,pyqtSignal
#####################################
#Own Implementations
from progressBar import ProgressWidget
from dirPath import get_dir_path
from objectSaveModule import objectProcessor
#####################################
# Notlar
# Progress bar gözükmüyor.Bu Problemi çöz/Çözüldü.Progress barın şeklini şemalini değer artışını adam gibi yap.
# Dosyalarıda kontrol et sadece dizin kontrolü var
class ML():
    def __init__(self,userIndex,calculate = False,data_dict = None,toReset = False,*args, **kwargs):
        self.userIndex = userIndex
        self.returnValue = False
        self.resetResult = False
        self.objProcessor = objectProcessor(userIndex = self.userIndex)
        ###########################3
        #Paths
        self.path = get_dir_path()
        self.userObjectFolderPath = "{}Objects/user{}/".format(self.path,hex(self.userIndex)[2:])
        self.userProgressionPercentFilePath = "{}progressionPercentage.pkl".format(self.userObjectFolderPath)

        self.userClassificationObjectFolderPath = "{}ClassificationObjects/".format(self.userObjectFolderPath)
        self.classificationObjectPath = "{}generalSituationEstimator.pkl".format(self.userClassificationObjectFolderPath)

        self.userRegressionObjectFolderPath = "{}RegressionObjects/".format(self.userObjectFolderPath)
        self.regressionObjectPath = "{}regressionsDict.pkl".format(self.userRegressionObjectFolderPath)        
        ###########################3
        



        if toReset:
            self.resetResult = self.objProcessor.resetUserData()
        else:
            if calculate and isinstance(data_dict,dict):#Tahmin yapma dururmu

                self.data_dict = data_dict# Bu bir problem ya da gereksiz
                self.predictable_data_dict = self.findPredictableFrames()
                
                if self.predictable_data_dict != dict(): # Şartları sağlayıp sağlamadığını kontrol eder. 

                    if not self.objProcessor.userOBJFolder(control=True):#Obje dizini olmayanlar
                        self.objProcessor.userOBJFolder(create=True)
                    else:
                        #Burada bir uyarı ekranı yap.Çünkü objeler yeniden tanımlanır.Hatta bir progress bar yap.
                        self.objProcessor.userOBJFolder(create=True,query=False)
                    
                    wid = ProgressWidget()
                    wid.show()
                    wid.addProgression(10,"[+] Verim tahmini algoritmaları için uygun veri oluşturuldu.")
                    #self.datasetAdjusterWithPCA() # Verimsizlik sağlar
                    self.generalClassificationDataset = self.generalSituationsDataset
                    print(self.generalClassificationDataset)
                    wid.addProgression(10,"[+] Genel aktivite tahmini algoritması için uygun veri oluşturuldu.")
                    self.algorithmDict = self.findBestRegression
                    wid.addProgression(40,"[+] Şartları sağlayan aktivitelerin verim tahmin algoritmaları oluşturuldu.")
                    self.classificationEstimator = self.findBestClassification
                    wid.addProgression(30,"[+] Genel aktivite tahmini algoritması oluşturuldu.")
                    self.objProcessor.saveObjects(self.classificationEstimator,self.algorithmDict)
                    wid.addProgression(10,"[+] Oluşturulan algoritma objeleri kaydedildi.")



                else :
                    #Eğer tahmin şartları sağlanmamış ise
                    pass

            else:#Tahmin isteme durumu
                if self.objProcessor.userOBJFolder(control=True):
                    self.classificationEstimator,self.algorithmDict = self.objProcessor.loadObjects()
                    self.returnValue = True
                
                else:
                    #Eğer ki daha tahmin algoritması çalışmamış ve objeler oluşmamış ise
                    self.returnValue = False
    
    def PCA_dim_reducter(self,dataset,n_components):
        model = PCA(n_components=n_components)
        reducted_dataset = model.fit_transform(dataset)
        return reducted_dataset

    def datasetAdjusterWithPCA(self):
        predictableNewDD = dict()
        for activity in self.predictable_data_dict:
            dataset = self.predictable_data_dict[activity]
            X = dataset[["isteklilik","yorgunluk","moral"]]#Bu kolonlar farklılık gösterebilir.
            y = dataset[["Efficiency"]]
            
            n_comp = len(X.columns)
            adj_X = self.PCA_dim_reducter(dataset = X,n_components = n_comp)
            adj_X = pd.DataFrame(data = adj_X,index=X.index,columns = X.columns)
            adj_dataset = pd.concat([adj_X,y],axis=1)
            predictableNewDD[activity] = adj_dataset
        
        self.predictable_data_dict = predictableNewDD

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
        #data = self.PCA_dim_reducter(dataset = data,n_components = len(data[0]))#Decorator olarak kullanmaya çalış

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

    def GiveGeneralActivity(self,data):#Burada gelen veriyi dimension reduction'dan geçirmenin bir yolunu bul.
        #data = self.PCA_dim_reducter(dataset = data,n_components = len(data[0]))
        activity = self.classificationEstimator.predict(data)

        return activity