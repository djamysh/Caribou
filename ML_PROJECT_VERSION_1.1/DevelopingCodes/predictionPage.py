#Arayüz Tasarım modülleri
from PyQt5.QtWidgets import (QWidget,QLineEdit,QLabel,QHBoxLayout,QVBoxLayout,
                            QTableView,QPushButton,QGraphicsDropShadowEffect,QApplication,QProgressBar)
from PyQt5.QtGui import QStandardItemModel,QStandardItem,QPixmap
from PyQt5.QtCore import Qt,QTimer
#Makine Öğrenmesi Modülü
from ML_Process import ML
from dirPath import get_dir_path
from recalculateButton import calculateButton

#Sistem modülü
import pickle

import sys
# Test edilmedi hatalar ve yarım kalmış OLABİLİR.
#Not
# İki kere çalışınca objeler siliniyor sebebi bul.Reset Fonksiyonunu test et.Buton boyutlarını ayarla


#Notlar
# ML objesinin calculate'si için özel bir buton ayarla.Bu buton tekrar tahmin devresinin çalışmasını sağlasın .
# PredictionForm'un sadece şartlar sağlandığı durumda açılması paradigmasını ortadan kaldır.Bunun yerine daha mantıklı bir şeyler koy.


# Tahmin devresi yeniden hesaplandıktan sonra eski sonuçları gizle
# Buton basıldıktan sonra bir temizle butonu olsun.
# Alert.png boyutu ile ilgilen
# Şartların sağlanmadığı durumu ile ilgilen
class PredictionForm(QWidget):
    def __init__(self,data_dict,userIndex,*args,**kwargs):
        super(PredictionForm,self).__init__()
        self.userIndex = userIndex
        self.path = get_dir_path()
        self.data_dict = data_dict #Parametre olan veri kümesinin sınıf attribute'si olması
        self.mlObj = ML(userIndex = self.userIndex)#Makine öğrenmesi sınıfına parametre olarak verinin gönderilmesi ve durumun
        self.objectExistence = self.mlObj.returnValue#Algoritmanın çalışıp çalışmadığı
        self.timer = QTimer()
        self.timer.timeout.connect(self.predictationTimers)
        self.timer.start(0)

        # hesaplanması.Bu satırın çalışması yaklaşık 7-10 saniye sürer.Çünkü obje çağrıldığında brute-force ile 
        # algoritmalar hesaplanır.
        self.setWindowTitle("Tahmin Formu")#Pencere Başlığı
        #self.setMaximumSize(396,419)#Pencere boyutları
        self.initUI()#Arayüz tasarım kodlarının çağrılması

    def initUI(self):
        #Layout'ların tanımlanması
        self.mainVerticalLayout = QVBoxLayout()
        self.mainVerticalLayout.setContentsMargins(6,6,6,6)
        self.headerLayout = QHBoxLayout()
        self.willingnessLayout = QHBoxLayout()
        self.fatigueLayout = QHBoxLayout()
        self.moraleLayout = QHBoxLayout()
        self.adviceLayout = QHBoxLayout()
        self.tableLayout = QHBoxLayout()
        #Widget'lerin tanımlanması,tasarlanması ve belirlenen layout'lara eklenmesi


        self.header = QLabel("Tahmin Formu")
        self.header.setStyleSheet("""background-color:#E2E7EE;color : #660022;
                font-size:32px;font-family: Courier;
                padding : 4px;""")
        self.headerLayout.addStretch()
        self.headerLayout.addWidget(self.header)
        self.headerLayout.addStretch()        

        styleSheetLabel = """font-family:Courier;font-weight:650;font-size:14px;
        color:#CDF1F9;background-color:#48234f;
        border-right:4px solid #065535;border-left:4px solid #065535;padding : 2px;"""
        styleSheetLineEdit = """font-family:Consolas;font-weight:550;font-size:12px;
        background-color:#400080;color:#FFF096;
        border:3px solid #96a5ff;padding : 2px;border-radius:3px;"""

        self.willingnessLabel = QLabel("Çalışma isteği")
        self.willingnessLabel.setStyleSheet(styleSheetLabel)
        self.willingnessLineEdit = QLineEdit()
        self.willingnessLineEdit.setStyleSheet(styleSheetLineEdit)
        self.willingnessLineEdit.setMaximumWidth(150)
        self.willingnessLineEdit.setMinimumWidth(150)

        self.willingnessLayout.addStretch()
        self.willingnessLayout.addWidget(self.willingnessLabel)
        self.willingnessLayout.addWidget(self.willingnessLineEdit)

        self.fatigueLabel = QLabel("Hissedilen yorgunluk")
        self.fatigueLabel.setStyleSheet(styleSheetLabel)
        self.fatigueLineEdit = QLineEdit()
        self.fatigueLineEdit.setStyleSheet(styleSheetLineEdit)
        self.fatigueLineEdit.setMaximumWidth(150)
        self.fatigueLineEdit.setMinimumWidth(150)

        self.fatigueLayout.addStretch()
        self.fatigueLayout.addWidget(self.fatigueLabel)
        self.fatigueLayout.addWidget(self.fatigueLineEdit)
        
        self.moraleLabel = QLabel("Moral")
        self.moraleLabel.setStyleSheet(styleSheetLabel)
        self.moraleLineEdit = QLineEdit()
        self.moraleLineEdit.setStyleSheet(styleSheetLineEdit)
        self.moraleLineEdit.setMaximumWidth(150)
        self.moraleLineEdit.setMinimumWidth(150)

        self.moraleLayout.addStretch()
        self.moraleLayout.addWidget(self.moraleLabel)
        self.moraleLayout.addWidget(self.moraleLineEdit)

        self.adviceButton = QPushButton("Tahminleri göster")
        self.adviceButton.setStyleSheet("""font-family:Courier;font-weight:650;font-size:14px;
        color: #ff003e;background-color:#00ffc1;
        border:1px solid #ffc100;border-radius:3px;padding:2px;""")
        shadow = QGraphicsDropShadowEffect(blurRadius=6, xOffset=5, yOffset=5)
        self.adviceButton.clicked.connect(self.advice)#Tahminleri gösterecek fonksiyonun çağrılması
        self.adviceButton.setGraphicsEffect(shadow)

        self.adviceLayout.addStretch()
        self.adviceLayout.addWidget(self.adviceButton)
        self.adviceLayout.addStretch()

        self.adviceResults1Header = QLabel("Çalışma Verimi Tahminleri")
        self.adviceResults1Header.setStyleSheet("""font-family:Courier;font-size:16px;font-weight:650;
        background-color : #725e51;color:#ffeeed;
        border-left:8px solid #065535;padding : 4px;""")

        self.adviceResults1Header.setMaximumWidth(300)
        self.adviceResults1Header.setHidden(True)

        self.adviceResults2Header = QLabel("Genel Aktivite Tahmini")
        self.adviceResults2Header.setStyleSheet("""font-family:Courier;font-size:16px;font-weight:650;
        background-color :	#516572;color:#ffeeed;
        border-left:8px solid #065535;padding : 4px;""")        
        self.adviceResults2Header.setMaximumWidth(300)
        
        self.adviceResults2Header.setHidden(True)

        self.table_view = QTableView()
        self.table_view.setHidden(True)
        self.tableLayout.addStretch()
        self.tableLayout.addWidget(self.table_view)
        self.tableLayout.addStretch()

        self.generalActLayout = QHBoxLayout()
        self.generalActLabel = QLabel()
        self.generalActLabel.setHidden(True)
        self.generalActLayout.addStretch()
        self.generalActLayout.addWidget(self.generalActLabel)
        self.generalActLayout.addStretch()
 
        self.mouseDoubleClickEvent = self.mouseDoubleClickEvent#Bu satır olmaz ise interface bu widgeti göstermez   
        

    
        self.alertLayout = QHBoxLayout()
        self.alertLabel = QLabel()
        self.alertImage = QLabel()
        
        self.alertImagePixmap = QPixmap("{}Images/siren.png".format(self.path))
        self.alertImagePixmap = self.alertImagePixmap.scaled(64,64,Qt.KeepAspectRatio)
        self.alertImage.setPixmap(self.alertImagePixmap)
        
        self.alertLabel.setHidden(True)
        self.alertImage.setHidden(True)

        self.calculateAlgorithmsButton = calculateButton(connectionFunction = self.calculateAlgorithms,iconPath="{}Images/calculator.png".format(self.path))
        self.toResetButton = calculateButton(connectionFunction = self.toReset,iconPath="{}Images/reset.png".format(self.path))

        self.alertLayout.addWidget(self.alertLabel)
        self.alertLayout.addWidget(self.alertImage)
        self.alertLayout.addWidget(self.calculateAlgorithmsButton)
        self.alertLayout.addWidget(self.toResetButton)

        #Tasarlanan layout'ların ana layout'a eklenmesi
        self.mainVerticalLayout.addStretch()
        self.mainVerticalLayout.addLayout(self.headerLayout)
        self.mainVerticalLayout.addLayout(self.willingnessLayout)
        self.mainVerticalLayout.addLayout(self.fatigueLayout)
        self.mainVerticalLayout.addLayout(self.moraleLayout)
        self.mainVerticalLayout.addLayout(self.adviceLayout)
        self.mainVerticalLayout.addWidget(self.adviceResults1Header)
        self.mainVerticalLayout.addLayout(self.tableLayout)
        self.mainVerticalLayout.addWidget(self.adviceResults2Header)
        self.mainVerticalLayout.addLayout(self.generalActLayout)
        self.mainVerticalLayout.addLayout(self.alertLayout)

        self.mainVerticalLayout.addStretch()
        self.setLayout(self.mainVerticalLayout)
    
    def toReset(self):
        result = ML(self.userIndex,toReset=True)
        self.predictionResultsVisibility(visibilty=False)
        if result or self.objectExistence:
            self.objectExistence = False
        else:
            self.objectExistence = False

    def predictationTimers(self):
        if self.objectExistence:
            self.alertLabel.setHidden(True)
            self.alertImage.setHidden(True)

        else:
            self.alertLabel.setText("Tahmin algoritmalarının hesaplanması gerekiyor.")
            self.alertLabel.setHidden(False)
            self.alertImage.setHidden(False)

    def predictionResultsVisibility(self,visibilty = False):
        vis = not bool(visibilty) 
        self.adviceResults1Header.setHidden(vis)
        self.table_view.setHidden(vis)
        self.adviceResults2Header.setHidden(vis)
        self.generalActLabel.setHidden(vis)

            

    def calculateAlgorithms(self):
        self.calculateAlgorithmsButton.setDisabled(True)

        self.mlObj = ML(userIndex = self.userIndex,data_dict = self.data_dict,calculate=True)#Makine öğrenmesi sınıfına parametre olarak verinin gönderilmesi ve durumun
        self.predictionResultsVisibility(visibilty=False)
        self.objectExistence = True
        self.calculateAlgorithmsButton.setEnabled(True)
    

    def efficiencyPredictionTable(self,data):
        #Bu fonksiyon veriyi tablo modeline çevirir ve modeli table_view'e atamasını yapar.
        model = QStandardItemModel()
        model.setRowCount(len(data))
        model.setColumnCount(1)
        model.setHorizontalHeaderLabels(["Verim"])
        rows = [str(d[0]) for d in data]
        model.setVerticalHeaderLabels(rows)

        index = 0
        for job,efficiency in data:
            if efficiency < 0 :
                efficiency = 0
            elif efficiency > 100:
                efficiency = 100

            item = QStandardItem("%"+str(efficiency))
            item.setFlags(Qt.ItemIsEnabled)
            model.setItem(index,0,item)
            index += 1

        self.table_view.setModel(model)
        self.table_view.setColumnWidth(0,40)
        self.table_view.setMaximumWidth(83)
        self.table_view.setMaximumHeight(111)
        #Scroll bar'ı kaldır.

    def advice(self):
        willingness = self.willingnessLineEdit.text()
        fatigue = self.fatigueLineEdit.text()
        morale = self.moraleLineEdit.text()
        #Hataların handle edilmesi
        try:
            willingness = int(willingness)
            if not(isinstance(willingness,int)):
                self.willingnessLineEdit.setText("1 ile 100 arasında bir sayı giriniz")
                return ""

            fatigue = int(fatigue)
            if not(isinstance(fatigue,int)):
                self.fatigueLineEdit.setText("1 ile 100 arasında bir sayı giriniz")                
                return ""

            morale = int(morale)            
            if not(isinstance(morale,int)):
                self.moraleLineEdit.setText("1 ile 100 arasında bir sayı giriniz")
                return ""

        except ValueError:
            return ""
            
        data =[[willingness,fatigue,morale]]
        adviceList = self.mlObj.giveMeAdvice(data)#Aktiviteye dayalı verimlerin bilgisini elde eder
        generalActivity = self.mlObj.GiveGeneralActivity(data)[0]#Genel aktivite ismini elde eder
        adviceList = [(job,round(float(efficiency))) for efficiency , job in adviceList]
        self.efficiencyPredictionTable(adviceList)
        self.generalActLabel.setStyleSheet("""
        font-family:Consolas;font-size:14px;font-weight:650;
        color:#e5e5e5;background-color:#555555;
        border:1px solid #065535;padding:2px;
        """)
        self.generalActLabel.setText(generalActivity)
        self.predictionResultsVisibility(visibilty=True)#Sonuçları gösterir


if __name__ == '__main__':
    import numpy.random as npr
    import pandas as pd
    activite1 = [
                [
                    npr.randint(45,60), #İsteklilik
                    npr.randint(30,40), #Yorgunluk
                    npr.randint(75,90), #Moral
                    npr.randint(65,80)  #Son Verim
                ]
                for i in range(20)]
    activite2 = [
            [
                npr.randint(15,20),
                npr.randint(35,45),
                npr.randint(45,60),
                npr.randint(50,65)
            ]
            for i in range(20)]

    activite3 = [
            [
                npr.randint(70,80),
                npr.randint(45,55),
                npr.randint(50,65),
                npr.randint(25,65)
            ]
            for i in range(20)]


    activite1 = pd.DataFrame(activite1,columns = ["isteklilik","yorgunluk","moral","Efficiency"],index = range(20))
    activite2 = pd.DataFrame(activite2,columns = ["isteklilik","yorgunluk","moral","Efficiency"],index = range(20))
    activite3 = pd.DataFrame(activite3,columns = ["isteklilik","yorgunluk","moral","Efficiency"],index = range(20))
    data_dict=  {"OP1":activite1,"OP2":activite2,"OP3":activite3}
    app = QApplication(sys.argv)
    obj = PredictionForm(data_dict,0)
    obj.show()
    sys.exit(app.exec_())
