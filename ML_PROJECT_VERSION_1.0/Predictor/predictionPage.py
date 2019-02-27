#Arayüz Tasarım modülleri
from PyQt5.QtWidgets import (QWidget,QLineEdit,QLabel,QHBoxLayout,QVBoxLayout,
                            QTableView,QPushButton,QGraphicsDropShadowEffect,QApplication)
from PyQt5.QtGui import QStandardItemModel,QStandardItem
from PyQt5.QtCore import Qt,QTimer
#Makine Öğrenmesi Modülü
from ML_Process import ML
#Sistem modülü
import sys

class PredictionForm(QWidget):
    def __init__(self,data_dict,*args,**kwargs):
        super(PredictionForm,self).__init__()
        self.data_dict = data_dict #Parametre olan veri kümesinin sınıf attribute'si olması
        self.mlObj = ML(self.data_dict)#Makine öğrenmesi sınıfına parametre olarak verinin gönderilmesi ve durumun
        # hesaplanması.Bu satırın çalışması yaklaşık 7-10 saniye sürer.Çünkü obje çağrıldığında brute-force ile 
        # algoritmalar hesaplanır.
        self.setWindowTitle("Tahmin Formu")#Pencere Başlığı
        self.setMaximumSize(386,409)#Pemcere boyutları
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
        self.generalActLayout.addStretch()
        self.generalActLayout.addWidget(self.generalActLabel)
        self.generalActLayout.addStretch()
 
        self.mouseDoubleClickEvent = self.mouseDoubleClickEvent#Bu satır olmaz ise interface bu widgeti göstermez   

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
        self.mainVerticalLayout.addStretch()
        self.setLayout(self.mainVerticalLayout)

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
            item = QStandardItem("%"+str(efficiency))
            item.setFlags(Qt.ItemIsEnabled)
            model.setItem(index,0,item)
            index += 1

        self.table_view.setModel(model)
        self.table_view.setColumnWidth(0,40)
        self.table_view.setMaximumWidth(73)
        self.table_view.setMaximumHeight(111)
        self.table_view.setHidden(False)

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
        self.adviceResults1Header.setHidden(False)
        self.adviceResults2Header.setHidden(False)
        self.efficiencyPredictionTable(adviceList)
        self.generalActLabel.setStyleSheet("""
        font-family:Consolas;font-size:14px;font-weight:650;
        color:#e5e5e5;background-color:#555555;
        border:1px solid #065535;padding:2px;
        """)
        self.generalActLabel.setText(generalActivity)
        


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
    obj = PredictionForm(data_dict)
    obj.show()
    sys.exit(app.exec_())
