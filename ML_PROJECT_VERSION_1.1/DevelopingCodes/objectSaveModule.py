from dirPath import get_dir_path
import shutil
import pickle
import os
import sys

class objectProcessor():
    def __init__(self,userIndex, *args, **kwargs):
        self.userIndex = userIndex

        self.path = get_dir_path()
        self.objectFolderPath = "{}Objects/".format(self.path)
        self.userObjectFolderPath = "{}Objects/user{}/".format(self.path,hex(self.userIndex)[2:])
        self.userProgressionPercentFilePath = "{}progressionPercentage.pkl".format(self.userObjectFolderPath)

        self.userClassificationObjectFolderPath = "{}ClassificationObjects/".format(self.userObjectFolderPath)
        self.classificationObjectPath = "{}generalSituationEstimator.pkl".format(self.userClassificationObjectFolderPath)

        self.userRegressionObjectFolderPath = "{}RegressionObjects/".format(self.userObjectFolderPath)
        self.regressionObjectPath = "{}regressionsDict.pkl".format(self.userRegressionObjectFolderPath)  

        self.createObjectPath()


    def resetUserData(self):
        if self.userOBJFolder(control=True):
            shutil.rmtree(self.userObjectFolderPath)
            return True
        else:
            return False

    def saveObjects(self,classificationEstimator,algorithmDict):

        #Objeler kayıt edilir
        pickle.dump(obj = classificationEstimator,file = open(self.classificationObjectPath,"wb"))
        pickle.dump(obj = algorithmDict,file = open(self.regressionObjectPath,"wb"))
    
    def loadObjects(self):
        classificationEstimator = pickle.load(open(self.classificationObjectPath,"rb"))
        algorithmDict = pickle.load(open(self.regressionObjectPath,"rb"))
        return (classificationEstimator,algorithmDict)
    
    def createObjectPath(self):
        try:
            os.mkdir(self.objectFolderPath)
        except FileExistsError:
            pass

        
    
    def userOBJFolder(self,control = False,create = False,query = True):


        if control:
            if (os.path.isdir(self.userObjectFolderPath) and 
            os.path.isdir(self.userClassificationObjectFolderPath) and
            os.path.isdir(self.userRegressionObjectFolderPath) and
            os.path.isfile(self.regressionObjectPath) and
            os.path.isfile(self.classificationObjectPath)):
                #kullanıcının obje ,regresyon,sınıflandırma dizininin bulunup bulunmadığını kontrol eder
                return True
            else:
                return False
            
        if create:
            if not self.userOBJFolder(control=True):#Yaratılıp yaratılmayacağını kontrol eder
                #Dizin yaratılır
                try:
                    os.mkdir(self.userObjectFolderPath)
                    os.mkdir(self.userClassificationObjectFolderPath)
                    os.mkdir(self.userRegressionObjectFolderPath)
                except FileExistsError:#Bazı durumlarda kullanıcı işlemi yarıda keserse burada hata çıkarabilir.
                    shutil.rmtree(self.userObjectFolderPath)
                    self.userOBJFolder(create=True)

            else:
                #Dizin sıfırlanır
                if query :
                    sys.stdout.write("[Warning] Object folder will be recreated.Current all objects will be lose.")
                    q = input("Are you sure about recreation ? (y/n) : ")
                else:
                    q = "y"

                if q == "y":
                    print("Segmentation Last")
                    shutil.rmtree(self.userObjectFolderPath)#Dosya ve içindekiler gider
                    self.userOBJFolder(create=True)#Boş dizinler yeniden yaratılır.

                else :
                    sys.stdout.write("[Info] Operation has been killed")
    