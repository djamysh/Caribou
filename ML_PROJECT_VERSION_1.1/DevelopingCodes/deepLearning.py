import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import OneHotEncoder,LabelEncoder,StandardScaler
from sklearn.cross_validation import train_test_split,KFold,cross_val_score
from sklearn.metrics import r2_score
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score,confusion_matrix

class DeepLearningStaff():
    def __init__(self,data_dict,*args, **kwargs):
        self.data_dict = data_dict
        self.predictable_data_dict = self.findPredictableFrames()
        self.datasetAdjusterWithPCA()
        self.regressors = dict()
        self.adjustRegressors()
        for i in self.regressors:
            print(i , "\t" , self.regressors[i])

    def adjustRegressors(self):
        for activity in self.predictable_data_dict:
            dataset = self.predictable_data_dict[activity]
            X = dataset.iloc[:,:-1]
            y = dataset.iloc[:,-1:]
            x_train,x_test,y_train,y_test = train_test_split(X,y,test_size = 0.33)
            print("Segment 0")
            regressorOfActivity  = self.build(x_train,y_train)
            print("Segment 1")
            y_pred = regrssorOfActivity.predict(x_test)
            print("Segment 2")
            r2 = r2_score(y_test,y_pred)
            print("r2 Score of {} activity : {}".format(activity,r2))
            self.regressors[activity] = regressorOfActivity



    def build(self,X,y):
        import keras
        from keras.models import Sequential
        from keras.layers import Dense
        from keras.wrappers.scikit_learn import KerasRegressor

        classifier = Sequential()
        classifier.add(Dense(6,activation="relu",init = "uniform",input_dim = 11))
        classifier.add(Dense(6,activation="relu",init = "uniform"))
        classifier.add(Dense(1,activation="sigmoid",init = "uniform"))

        classifier.compile(optimizer="Adam",loss ="categorical_crossentropy",metrics=["categorical_accuracy"])
        classifier.fit(X,y,epochs=50)
                
        return classifier


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

    def PCA_dim_reducter(self,dataset,n_components):
        model = PCA(n_components=n_components)
        reducted_dataset = model.fit_transform(dataset)
        return reducted_dataset

    def datasetAdjusterWithPCA(self):
        predictableNewDD = dict()
        for activity in self.predictable_data_dict:
            dataset = self.predictable_data_dict[activity]
            X = dataset[["isteklilik","yorgunluk","moral"]]
            y = dataset[["Efficiency"]]
            
            n_comp = len(X.columns)
            adj_X = self.PCA_dim_reducter(dataset = X,n_components = n_comp)
            adj_X = pd.DataFrame(data = adj_X,index=X.index,columns = X.columns)
            adj_dataset = pd.concat([adj_X,y],axis=1)
            predictableNewDD[activity] = adj_dataset
        
        self.predictable_data_dict = predictableNewDD    
            


if __name__ == "__main__":    
    import numpy.random as npr
    activite1 = [
                [
                    npr.randint(45,60), #İsteklilik
                    npr.randint(30,40), #Yorgunluk
                    npr.randint(75,90), #Moral
                    npr.randint(65,80)  #Son Verim
                ]
                for i in range(100)]
    activite2 = [
            [
                npr.randint(15,20),
                npr.randint(35,45),
                npr.randint(45,60),
                npr.randint(50,65)
            ]
            for i in range(100)]

    activite3 = [
            [
                npr.randint(70,80),
                npr.randint(45,55),
                npr.randint(50,65),
                npr.randint(25,65)
            ]
            for i in range(100)]


    activite1 = pd.DataFrame(activite1,columns = ["isteklilik","yorgunluk","moral","Efficiency"],index = range(100))
    activite2 = pd.DataFrame(activite2,columns = ["isteklilik","yorgunluk","moral","Efficiency"],index = range(100))
    activite3 = pd.DataFrame(activite3,columns = ["isteklilik","yorgunluk","moral","Efficiency"],index = range(100))
    data_dict=  {"OP1":activite1,"OP2":activite2,"OP3":activite3}
    obj = DeepLearningStaff(data_dict)