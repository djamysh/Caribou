import numpy as np
import pandas as pd 
import matplotlib as plt 

from sklearn.preprocessing import OneHotEncoder,LabelEncoder

########################################33
#Data columns : İsteklilik,Yorgunluk,Moral,Verim
#İsteklilik ==> 
class categoricPrediction():
    def __init__(self,data,*args, **kwargs):
        self.data = data

        self.preprocess1 = self.preprocces_section1()#RETURNS TUPLE
        self.concattedFeatures = self.concatedData()


    def preprocces_section1(self):
        #Regrtive to clasificative
        isteklilik = self.data.iloc[:,0]
        yorgunluk =  self.data.iloc[:,1]
        moral =  self.data.iloc[:,2]
        verim =  self.data.iloc[:,3]

        istNew = list()
        for value in isteklilik.values:
            if value <50 :
                istNew.append(np.float(0))
            else:
                istNew.append(np.float(0))
        isteklilik = pd.DataFrame(np.array(istNew).reshape((len(istNew),1)),columns = ["İsteklilik"])

        yorgNew = list()
        for value in yorgunluk.values:
            if value < 33:
                yorgNew.append("yorgun")
            elif value>= 33 and value <66:
                yorgNew.append("normal")
            else:
                yorgNew.append("dinç")
        yorgunluk = pd.DataFrame(np.array(yorgNew).reshape((len(yorgNew),1)),columns = ["Yorgunluk"])
        
    

        moralNew = list()
        for value in moral.values:
            if value < 25:
                moralNew.append("l")
            elif value>= 25 and value <50:
                moralNew.append("m")
            elif value>= 50 and value <75:
                moralNew.append("n")
            else:
                moralNew.append("h")

        moral = pd.DataFrame(np.array(moralNew).reshape((len(moralNew),1)),columns = ["Moral"])



        verimNew = list()
        for value in verim.values:
            if value<=50:
                verimNew.append(np.float(0))
            
            elif value>50 and value<=100:
                verimNew.append(np.float(1))
        verim = pd.DataFrame(np.array(verimNew).reshape((len(verimNew),1)),columns = ["Verim"])

        
        return (isteklilik,yorgunluk,moral,verim)
        
    def preprocces_section2(self):
        try:

            isteklilik,yorgunluk,moral,verim = self.preprocess1
            fo



        except NameError:
            print("[HATA] İlk Ön işleme hesaplanmamış.")

    def concatedData(self):
        concattedFeatures=pd.concat([self.preprocess1[0],self.preprocess1[1],self.preprocess1[2],self.preprocess1[3]],axis = 1)
        return concattedFeatures