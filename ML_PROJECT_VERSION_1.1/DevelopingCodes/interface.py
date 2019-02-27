#Arayüz tasarım modülleri
from PyQt5.QtWidgets import (QWidget , QLabel , QLineEdit , QTableWidget,
                            QTableWidgetItem , QHBoxLayout , QVBoxLayout , QGraphicsDropShadowEffect ,
                            QComboBox , QPushButton , QDateEdit , QMenu , QInputDialog,QApplication)
from PyQt5.QtCore import Qt,QTimer,QDate,QRect,pyqtSlot
from PyQt5.QtGui import QPixmap,QColor
from PyQt5.QtCore import QEvent

#Kendi implementasyonumuz olan modüller
from dirPath import get_dir_path
    #Veri işleme modüller
from sqliteModule import sql_functions
from preproccesingForDB import preproccesedData
    #Arayüz tasarım modüller
from predictionPage import PredictionForm
from JobInfoWidget import JobInfo
from timeRange import newTimeRange

#Diğer modüller
import time
import re
import datetime
import sys 
import os


#Tutarsız girdi problemi çözüldü
#Girdi işlemesine geçiliyor
class mainScreen(QWidget):
    def __init__(self,userIndex, *args, **kwargs):
        super().__init__()

        self.dir_path = get_dir_path()
        self.userIndex = userIndex
        self.databasePath ="{}Databases/user{}.db".format(self.dir_path,hex(self.userIndex)[2:])

        self.dbObj = sql_functions(self.databasePath)#Kullanıcının günlük aktivite bilgilerinin saklandığı veritabanına bağlanılır

        self.rangeCount = 0
        self.last = None

        self.ranges = list()
        self.jobNames = list()
        self.data_dict= None

        self.dataTypes = [(str,"str"),(str,"str"),(int,"int"),(int,"int"),(int,"int"),(int,"int")]
        self.predictionVariables = ["Aktivite Adı","İsteklilik","Yorgunluk","Moral","Son Verim"]
        self.dayVariables = ["Date","TimeRange","Willingness","Fatigue","Morale","Efficiency"]
        self.sleepVariables = ["Date","SleepRange","SleepEfficiency"]
        self.newDateDBConfigurationText = "('Job','TEXT'),('TimeRange','TEXT'),('Willingness','INT'), ('Fatigue','INT'), ('Morale','INT'),('Efficiency','INT')"
        self.setWindowTitle("Proje")


        self.initUI()

    def initUI(self):
        ############################
        # Layout'ların tanımlanması
        self.mainVerticalLayout = QVBoxLayout()
        self.upHorizontalLayout = QHBoxLayout()
        self.middleHorizontalLayout = QHBoxLayout()
        self.middleHorizontalLayoutRightVerticalLayout = QVBoxLayout()
        self.downHorizontalLayout = QHBoxLayout()
        self.predictionLayout = QHBoxLayout()

        #Gölgeler
        shadow = QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3)
        shadow2 = QGraphicsDropShadowEffect(blurRadius=6, xOffset=5, yOffset=5)

        
        #Widget'lerin tanımlanması,tasarlanması ve layout'lara eklenemesi
        
        
        ############################
        self.imageCheckout = QLabel()
        self.textCheckout = QLabel()

        ############################

        self.sleepLabel = QLabel()
        self.sleepLabel.setText("Uyku Saatleri :")
        self.sleepLabel.setMaximumWidth(150)
        self.sleepLabel.setStyleSheet("""
        color :#f2f3f4;
        background-color:#3b444b;
        border-left:4px Solid  #a52a2a;
        border-right:4px Solid  #a52a2a;
        padding:4px;
        font-size:14px;
        font-family:Courier;
        border-radius:1px;
        font-weight:650;
        """)
        self.sleepLabel.setGraphicsEffect(shadow)

        sep0 = QLabel(":")
        sep1 = QLabel(":")
        sep2 = QLabel("-")
        

        self.sleepLabelhourCombo1 = QComboBox()
        self.sleepLabelhourCombo2 = QComboBox()

        for i in range(24):
            if i<10:
                element = "0"+str(i)
            else:
                element = str(i)
            self.sleepLabelhourCombo1.addItem(element,i)#element,index
            self.sleepLabelhourCombo2.addItem(element,i)#element,index

        self.sleepLabelMinuteCombo1 = QComboBox()
        self.sleepLabelMinuteCombo2 = QComboBox()

        for i in range(60):
            if i<10:
                element = "0"+str(i)
            else:
                element = str(i)
            self.sleepLabelMinuteCombo1.addItem(element,i)
            self.sleepLabelMinuteCombo2.addItem(element,i)

        
        
        self.ComboHorizontalLayout = QHBoxLayout()

        self.ComboHorizontalLayout.addWidget(self.sleepLabelhourCombo1)
        self.ComboHorizontalLayout.addWidget(sep0)
        self.ComboHorizontalLayout.addWidget(self.sleepLabelMinuteCombo1)
        self.ComboHorizontalLayout.addWidget(sep2)
        self.ComboHorizontalLayout.addWidget(self.sleepLabelhourCombo2)
        self.ComboHorizontalLayout.addWidget(sep1)
        self.ComboHorizontalLayout.addWidget(self.sleepLabelMinuteCombo2)
        self.ComboHorizontalLayout.addStretch()
            
        self.sleepEfficiencyLabel = QLabel()
        self.sleepEfficiencyLabel.setText("Uyku verimi : ") 
        self.sleepEfficiencyLabel.setStyleSheet("""
        color :#f2f3f4;
        background-color:#3b444b;
        border-left:4px Solid  #a52a2a;
        border-right:4px Solid  #a52a2a;
        padding:4px;
        font-size:14px;
        font-family:Courier;
        border-radius:1px;
        font-weight:650;
        """)
        self.sleepEfficiencyLabel.setMaximumWidth(150)
        self.sleepEfficiencyLabel.setGraphicsEffect(shadow)
        self.sleepEfficiency = QLineEdit()
        self.sleepEfficiency.setMaximumWidth(168)
        self.sleepEfficiency.setText("0-100")


        self.addRange = QPushButton()    
        self.addRange.setText("Yeni saat aralığı ekle")
        self.addRange.setStyleSheet("""
        font-family : "Times New Roman";
        font-size : 14px;
        font-weight:650;
        background-color:#065535;
        color:#ffc100;
        
        
        """)
        self.addRange.setMaximumWidth(150)
        self.addRange.setGraphicsEffect(shadow)

        self.addRange.clicked.connect(lambda : self.changeHorizontalHeader(-1))

        ############################
        self.Date = QDateEdit()
        date = QDate()
        currentDate = date.currentDate()
        self.Date.setDate(currentDate)
        ############################

        ############################
        self.profileButton = QPushButton("Profil")
        self.profileButton.clicked.connect(self.profilePageRedirection)
        ############################


        self.downHorizontalLayout.addStretch()
        self.save = QPushButton()
        self.save.setText("Kaydet")
        self.save.setGraphicsEffect(shadow)
        self.save.setStyleSheet("""
        color : #A52A2A;
        font-weight:bold;
        """)
        self.save.clicked.connect(self.saveToDataBase) #Bilgileri veritabanına kaydeden fonksiyonun çağrılması
        ############################


            #Zamalayıcılar
        ############################
        self.timer = QTimer()
        self.timer.timeout.connect(self._update)
        self.timer.start(1000)

        self.timer_job = QTimer()
        self.timer_job.timeout.connect(self.predictionButtonControl)
        self.timer_job.start(1000)

        self.fittedColumnsTimer = QTimer()
        self.fittedColumnsTimer.timeout.connect(self.AlltimeFittedColumns)
        self.fittedColumnsTimer.start(1000)


        ############################

            #Tablo
        self.tableWidget = QTableWidget()
        self.tableWidget.setGeometry(QRect(0, 40, 801, 511))
        self.tableWidget.setRowCount(len(self.predictionVariables))
        self.tableWidget.horizontalHeader().sectionDoubleClicked.connect(self.changeHorizontalHeader)

        self.tableWidget.setVerticalHeaderLabels(self.predictionVariables)
        ############################

        self.efficiencyPredictionButton = QPushButton()
        self.efficiencyPredictionButton.setMaximumWidth(160)
        self.efficiencyPredictionButton.clicked.connect(self.efficiencyPredictionButtonFunction)#Eğer gerekli şartlar sağlanmış ise tahmin şartları sağlanmış ise tahmin sayfasına yönledirecek fonksiyon
        self.efficiencyPredictionButton.setText("Tahmin Sayfası")
        self.efficiencyPredictionButton.setGraphicsEffect(shadow2)
        self.efficiencyPredictionButton.setStyleSheet("""
        font-family:"Times New Roman";
        font-size:14px;
        font-weight: 650;
        color: #d1b9c7;
        background-color: #130015;
        """)
        self.predictionLayout.addWidget(self.efficiencyPredictionButton)        
        


    
        self.upHorizontalLayout.addWidget(self.Date)
        self.upHorizontalLayout.addStretch()
        self.upHorizontalLayout.addWidget(self.profileButton)
    
        self.middleHorizontalLayout.addWidget(self.tableWidget)

        self.middleHorizontalLayoutRightVerticalLayout.addWidget(self.addRange)
        self.middleHorizontalLayoutRightVerticalLayout.addWidget(self.sleepLabel)
        self.middleHorizontalLayoutRightVerticalLayout.addLayout(self.ComboHorizontalLayout)
        self.middleHorizontalLayoutRightVerticalLayout.addWidget(self.sleepEfficiencyLabel)
        self.middleHorizontalLayoutRightVerticalLayout.addWidget(self.sleepEfficiency)
        self.middleHorizontalLayoutRightVerticalLayout.addLayout(self.predictionLayout)
        self.middleHorizontalLayoutRightVerticalLayout.addStretch()

        self.downHorizontalLayout.addWidget(self.textCheckout)
        self.downHorizontalLayout.addWidget(self.imageCheckout)     
        self.downHorizontalLayout.addWidget(self.save)     
        
        self.middleHorizontalLayout.addLayout(self.middleHorizontalLayoutRightVerticalLayout)

        #Oluşturulan Layout'ların ana layouta eklenmesi
        self.mainVerticalLayout.addLayout(self.upHorizontalLayout)
        self.mainVerticalLayout.addLayout(self.middleHorizontalLayout)
        self.mainVerticalLayout.addLayout(self.downHorizontalLayout)
        
        self.newrangeWidget = newTimeRange()
        self.newrangeWidget.setHidden(True)
        self.newrangeWidget.newRangeSignal.connect(self.getNewRange)
        self.mainVerticalLayout.addWidget(self.newrangeWidget)

        #Tablo boyutlarının ayarlanması
        self.tableWidget.setMaximumWidth(666)
        self.tableWidget.setMinimumWidth(286)

        self.tableWidget.setMaximumHeight(180)
        self.tableWidget.setMinimumHeight(180)
        self.setMaximumHeight(171) 

        self.setLayout(self.mainVerticalLayout)
        #Tablo ismine'sağ tıklandığında menu açılmasını sağlayan kod parçası 
        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)#
        self.tableWidget.customContextMenuRequested.connect(self.generateMenu)
        self.tableWidget.viewport().installEventFilter(self)
        ##################################

    def eventFilter(self, source, event):#gelen event'ı filtreler ve eğer event aktivite ismine sağ tıklama ise menu açığa çıkartır.
        if(event.type() == QEvent.MouseButtonPress and
           event.buttons() == Qt.RightButton and
           source is self.tableWidget.viewport()):
            item = self.tableWidget.itemAt(event.pos())

            if item is not None and item.row() == 0:
                self.menu = QMenu(self)
                

                self.menu.addAction("Aktivite bilgisi")
                self.menu.addAction("Aktiviteyi sil")
                self.menu.triggered.connect(self.menuActions)#Menu aksiyonlarına yönlendirir.

            else:
                self.menu = QMenu(self)

        return super(mainScreen, self).eventFilter(source, event)

    def generateMenu(self, pos):
        self.menu.exec_(self.tableWidget.mapToGlobal(pos)) 

    def menuActions(self,action):
        action = action.text()

        if action == "Aktiviteyi sil":# aksiyon bu ise seçili aktivite kolonu veritabanından ve arayüz tablosundan silinir.
            timeRangeIndex = self.tableWidget.currentColumn()
            timeRange = self.ranges[timeRangeIndex]
            date = self.getValidDate()
            self.dbObj.delete_row(date,"TimeRange",timeRange)
            self._update(specialSynchronize=True)

        elif action == "Aktivite bilgisi":# aksiyon bu ise seçili aktivitenin bilgilerinin göstildiği sayfa açılır.
            activity = self.tableWidget.currentItem().text()
            needToDo = 15

            try:
                data = self.data_dict[activity]
                doneTimes = len(data.index)
                
            except KeyError:
                doneTimes = 0
            
            finally:
                popWindow = JobInfo(activity = activity,doneTimes=doneTimes,needToDo=needToDo)
                popWindow.show()

    def efficiencyPredictionButtonFunction(self):#verim tahmin sayfasına yönlendirir.
        popWindow = PredictionForm(self.data_dict,self.userIndex)
        popWindow.show()

    def findSeperator(self,data):# Verideki ayracı bulur
        seperator = re.findall("\D",data)[0]
        return seperator

    def rangeAmounts(self,ranges): #saat aralık miktarlarını döndürür. 
        amounts = list()
        for i in ranges:
            if i != "[*]":
                data = tuple(i.split("-"))
                start = data[0].split(":")
                end = data[1].split(":")
                amount = self.diffrenceBetweenTwoHour(start,end)
                amounts.append(amount)

        return amounts

    def predictionButtonControl(self):# Eldeki veri kümesinin tahmin şartlarını sağlayıp sağlamadığına bakar ve buna göre tahmin formu butonunu aktive eder ya da tam tersi.
        obj = preproccesedData(dayTableColumns=self.dayVariables,sleepTableColumns=self.sleepVariables,rawDatabasePath=self.databasePath)
        data = obj.get_data_Dict

        # Veri kümesinin kullanılabilirliği şartı ise en az iki ayrı aktivite kümesi olması ve her aktivite kümesinin en az  elemanının olmasıdır.
        usableDatasetCount = 0 # Kullanılabilir aktivite küme sayısını bulur.
        for key in data:
            specifedDataSet = data[key]
            if len(specifedDataSet.index) < 15:
                pass
            else:
                usableDatasetCount += 1
        
        if usableDatasetCount < 2:# Eğer 2 tane ya da daha fazla ise tahmin form butonu kilidi kalkar
            self.efficiencyPredictionButton.setDisabled(True)
        else:
            self.efficiencyPredictionButton.setEnabled(True)

            

        self.data_dict = data


    def diffrenceBetweenTwoHour(self,hour1 ,hour2 = (0,0),data_splittation = False):#İki saat arasındaki otomatik olarak bulur      
        if data_splittation:
            hour1,hour2 = [hour.split(":") for hour in hour1.split("-")]

        h1 = int(hour1[0])
        m1 = int(hour1[1])

        h2 = int(hour2[0])
        m2 = int(hour2[1])

        d1 = datetime.timedelta(hours = h1,minutes = m1)
        d2 = datetime.timedelta(hours = h2,minutes = m2)

        amount = d2 - d1
        amount = amount.seconds/60/60

        return amount
    
    def profilePageRedirection(self):
        from ProfilePage import Profile
        popWindow = Profile(self.userIndex)
        popWindow.show()





    def getValidDate(self,makeINT = 0):#Şu anki seçili tarihi parametrelere göre döndürür.
        date = self.Date.dateTime().toPyDateTime().date()
        if bool(makeINT):
            date = [int(i) for i in str(date).split("-")][::-1]
        else:
            dateN = ""
            for var in str(date).split("-")[::-1]:dateN+=var+"-"
            dateN = dateN[:-1]
            date = dateN

        return date
    def usableClock(self,range_):#Saat aralığını kullanılabilir hale getirir.
        h1,h2 = range_.split("-")
        h1 = h1.split(":")
        h2 = h2.split(":")

        return (h1,h2)

    def inputControlAffecters(self,inData):
        try:
            inp = int(inData)
            if (inp > 100) or (inp < 0):
                return False
            return True
        except ValueError:
            return False



    def _update(self,specialSynchronize = False):#Otomatik olarak tabloyu veritabanındaki bilgiler ile doldurur.

        date = self.getValidDate(makeINT=1)#Sayısal olan
        if not(self.last == date) or specialSynchronize:
            tableName = self.getValidDate()#Veritabanı kodunda kullanılabilir olan
            self.ranges = list()
            self.last = date

            sleepDataDates = [tup[0].split(self.findSeperator(tup[0])) for tup in self.dbObj.get_column_by_name("SleepTable","Date")]
            sleepDataDates = [[int(element) for element in upElement] for upElement in sleepDataDates]
            controlDate = [int(element) for element in date]
            if controlDate in sleepDataDates:
                row = self.dbObj.get_row("SleepTable","Date",tableName)
                range_,efficiency_ = row[1],row[2]
                self.sleepEfficiency.setText(str(efficiency_))
                
                h1,h2 = self.usableClock(range_)
                self.sleepLabelhourCombo1.setCurrentIndex(int(h1[0]))
                self.sleepLabelMinuteCombo1.setCurrentIndex(int(h1[1]))
                self.sleepLabelhourCombo2.setCurrentIndex(int(h2[0]))
                self.sleepLabelMinuteCombo2.setCurrentIndex(int(h2[1]))

            
            else:
                self.sleepEfficiency.setText("0-100")
                self.sleepLabelhourCombo1.setCurrentIndex(0)
                self.sleepLabelhourCombo2.setCurrentIndex(0)
                self.sleepLabelMinuteCombo1.setCurrentIndex(0)
                self.sleepLabelMinuteCombo2.setCurrentIndex(0)




            
            createControl = 0
            existanceControl = 0
            for tup in self.dbObj.tableList():
                try:
                    element = tup[0]
                    seperator = self.findSeperator(element)
                    element = [int(i) for i in element.split(seperator)]
                    if (date == element) and (self.dbObj.get_row_count(tableName) > 0):
                        createControl = 1
                        existanceControl = 1

                    else:
                        pass
                except ValueError:
                    pass

            if not(createControl):#Eğer tablo yoksa yaratlılır.
                exec("self.dbObj.create_table(tableName,{})".format(self.newDateDBConfigurationText))#Hata olmaması için tablo yaratlılır
            


            if existanceControl:
                for tup in self.dbObj.tableList():
                    try:
                        columns = self.dbObj.get_columns(tup[0])
                        hourRanges = self.dbObj.get_column_by_name(tableName,"TimeRange")
                        hourRanges = [tup[0] for tup in hourRanges]
                        self.ranges = hourRanges
                        self.tableWidget.setColumnCount(len(hourRanges))
                        self.tableWidget.setHorizontalHeaderLabels(hourRanges)


                        columns.remove("TimeRange")
                        indexX = 0
                        for column in columns:
                            rows = self.dbObj.get_column_by_name(tableName,column)
                            rows = [tup[0] for tup in rows]
                            indexY = 0
                            for row in rows:
                                self.tableWidget.setItem(indexX,indexY,QTableWidgetItem(str(row)))
                                indexY += 1
                            
                            indexX += 1
                    
                    except ValueError:
                        pass
                
                RangeAmounts = self.rangeAmounts(hourRanges)
                for index in range(len(RangeAmounts)):
                    self.tableWidget.setColumnWidth(index,self.tableWidget.columnWidth(index)*RangeAmounts[index])



            else:# Eğer seçili güne dair bir bilgi yok ise bu devre çalışır.

                self.tableWidget.clear()
                self.tableWidget.setVerticalHeaderLabels(self.predictionVariables)
                self.tableWidget.setColumnCount(1)
                
                self.tableWidget.setHorizontalHeaderLabels(["[\u2795]"])
                
                
    def AlltimeFittedColumns(self):#Kolon uzunluklarının her zaman sabit kalmasını sağlar
        for index in range(self.tableWidget.columnCount()):
            self.tableWidget.setColumnWidth(index,100)


    def getSleepRangefromCombo(self):#Combobox değerlerini string şeklinde döndürür.
        range_ = self.sleepLabelhourCombo1.currentText()+":"+self.sleepLabelMinuteCombo1.currentText()+"-"+self.sleepLabelhourCombo2.currentText()+":"+self.sleepLabelMinuteCombo2.currentText()
        return range_

    def saveToDataBase(self):#Seçili tarihte girili bilgileri veritabanınına kayıt eder.

        date = self.getValidDate()
        sleepDataDates = [tup[0].split(self.findSeperator(tup[0])) for tup in self.dbObj.get_column_by_name("SleepTable","Date")]
        separetedDate = date.split(self.findSeperator(date))

        try:#Eğer uyku verimi değişkenine geçersiz değer girilirse...

            sleepEf = int(self.sleepEfficiency.text())
            sleepRa =  self.getSleepRangefromCombo()
            
        except ValueError:
            self.sleepEfficiency.setText("Uyku verimi kısmı 1 ile 100 arasında sayısal bir değer alır.Başka bir veritipi girişi tespit edildi...")
            return 0 
        
        if separetedDate in sleepDataDates:
                self.dbObj.delete_row("SleepTable","*Date",date)
                self.dbObj.insert_data("SleepTable",date,sleepRa,sleepEf)

        else:
            self.dbObj.insert_data("SleepTable",date,sleepRa,sleepEf)


        if self.dbObj.get_row_count(date):
            for dif in self.ranges:
                if dif != "":
                    self.dbObj.delete_row(date,"*TimeRange",dif)
                else:
                    pass

        if self.dbObj.get_row_count(date):
            pass 
        else:
            pass 


        timeRanges = self.ranges
        errorColumns = list()
        if len(timeRanges) != 0:
            column_index = 0
            for column in range(self.tableWidget.columnCount()):
                rangeData = timeRanges[column]
                if rangeData != "[\u2795]" and rangeData != "" and self.splitableHourCheck(rangeData):
                    data= list()
                    index = 0
                    for row in range(self.tableWidget.rowCount()):
                        try:
                            inf = self.tableWidget.item(row,column).text()                            
                            if row == 0:
                                pass 
                            else:
                                position = (row,column)
                                ability = self.inputControlAffecters(inf)
                                if ability:
                                    pass
                                else:
                                    self.showError("Geçersiz formatta bilgi girişi.Hata kaynağı konumu : {}".format(position))
                                    return 0

                                

                            
                        except AttributeError:
                            nowD = [self.dataTypes[0]]+self.dataTypes[2:]
                            if nowD[index][0] == str:
                                inf = ""
                            else :
                                inf = 0
                        
                        data.append(inf)
                        index += 1


                    data.insert(1,rangeData)
                    dataChanged = list()
                    for iteration,dtype in zip(data,self.dataTypes):#Veri tipleri düzenenir..
                        if not isinstance(iteration,dtype[0]):
                            try:
                                iteration = eval("{}(iteration)".format(dtype[1]))
                            except ValueError:
                                pass
                        
                        dataChanged.append(iteration)
                    self.dbObj.insert_data(date,*data)#Bilginin veritabanına yüklenmesi
                else:
                    errorColumns.append(column_index)
                column_index += 1
        
        #Kullanıcıya kayıtın başarı durumunun bildirilmesi
        if not bool(len(errorColumns)):

            self.showSuccess("Bilgiler kaydedilmiştir.")


        else:
            columnsText =""
            for i in errorColumns:
                columnsText += str(i+1)+","
            
            columnsText = columnsText[:-1]

            self.showError("Geçersiz saat aralığı girişi.Hata kaynağı sütunları : {} ".format(columnsText))


    def showSuccess(self,message):
        self.textCheckout.setText(message)
        self.textCheckout.setStyleSheet("""
        font-family:Courier;
        font-size:14px;
        font-weight:650;
        color :#5A2C63;
        background-color:#C4FFC1;
        border-left:4px solid  	#35632c;
        padding : 4px;
        """)
        self.imageCheckout.setPixmap(QPixmap("{}Images/tickIconAdjusted.png".format(self.dir_path)))
        QTimer.singleShot(3000,lambda:self.textCheckout.setText(""))
        QTimer.singleShot(3000,lambda:self.textCheckout.setStyleSheet(""))
        QTimer.singleShot(3000,lambda:self.imageCheckout.setPixmap(QPixmap()))        

    def showError(self,errorMessage):
            self.textCheckout.setText(errorMessage)
            self.textCheckout.setStyleSheet("""
            font-family:Courier;
            font-size:14px;
            font-weight:650;
            color:#d22323;
            background-color:#f4919f;
            border-left:8px solid  #4F646B;
            padding:6px;  
            
            """)
            self.imageCheckout.setPixmap(QPixmap("{}Images/error.png".format(self.dir_path)))
            QTimer.singleShot(4000,lambda:self.textCheckout.setText(""))
            QTimer.singleShot(4000,lambda:self.textCheckout.setStyleSheet(""))
            QTimer.singleShot(4000,lambda:self.imageCheckout.setPixmap(QPixmap()))

    def splitableHourCheck(self,data):#Saat girdisinin bölünebilirliğini kontrol eder
        try:
            h1,h2 = [hour.split(":") for hour in data.split("-")]
            if (len(h1) and len(h2)) == 2:
                return True
            
            else:
                return False
        except:
            return False

    def changeHorizontalHeader(self,index):
        #Yeni saat aralığının girilmesi
        #Saat aralığı girilirken şu şekil kullanılmalıdır:
        # AA:BB-CC:DD
        # Aksi takdirde kodlar veri tabanına hata ortaya çıkar.
        
        if index == -1:
            index= self.tableWidget.columnCount()
            if index == 1 and self.ranges == []  :#and self.tableWidget.horizontalHeader.labels == "[\u2795]"
                index = 0
            
            else:
                # Eğer tabloda saat aralığı yok ise otomatik eklenen kolon sıkıntı yaratacaktır.
                # Bu sebeple index sıfıra eşitlenir.
                pass
        self.horizontalHeaderIndex = index

        self.newrangeWidget.setHidden(False)


    @pyqtSlot(str)
    def getNewRange(self,newRange):#Düzenlemeleri yap
        if newRange:
            try:
                time = [hour.split(":") for hour in newRange.split("-")]#Çalışma verimi
                self.tableWidget.setColumnWidth(self.horizontalHeaderIndex,150)
                self.ranges.append(newRange)
                self.tableWidget.setColumnCount(len(self.ranges))
                self.tableWidget.setHorizontalHeaderLabels(self.ranges)
            except IndexError:
                pass
        else:
            pass            

        self.newrangeWidget.cleanInputs()
        self.newrangeWidget.setHidden(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    obj = mainScreen(0)
    obj.show()
    sys.exit(app.exec_())


