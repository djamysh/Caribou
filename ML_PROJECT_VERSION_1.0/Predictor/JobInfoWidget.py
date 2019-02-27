#Modüllerin Yüklenmesi
#Arayüz modülleri
from PyQt5.QtWidgets import QWidget,QHBoxLayout,QVBoxLayout,QLineEdit,QLabel
#Sistem modülleri
import sys

class JobInfo(QWidget):
    def __init__(self,activity,doneTimes,needToDo,*args, **kwargs):
        super().__init__()
        #Girdilerin işlenmesi edilmesi.
        self.activity = str(activity)
        self.doneTimes = str(doneTimes)
        self.needToDo =  str(needToDo)

        #Pencere boyutlarının ayarlanması
        self.setMaximumSize(213,87)
        self.setMinimumSize(213,87)
        #Pencere başlığının girilmesi
        self.setWindowTitle("Aktivite Bilgileri")

        #Arayüz kodlarının çaılştırılması
        self.initUI()

    def initUI(self):
        #Layout Tasarımı
        self.mainVerticalLayout = QVBoxLayout()
        self.mainVerticalLayout.setContentsMargins(3,3,3,3)#3px'lik margin konulması
        self.acttextLayout = QHBoxLayout()
        self.middleHoriziontalLayout = QHBoxLayout()
        self.upHorizontalLayout = QHBoxLayout()

        #Label ve LineEdit widget'lerin tanımlanması layout'lara eklenmesi

        self.activityLabel = QLabel()
        self.activityLabel.setText(" Aktivite :")
        self.activityName = QLineEdit() 
        self.activityName.setText(self.activity)
        self.activityName.setReadOnly(True)
        self.activityName.setMaximumWidth(300)
        self.acttextLayout.addWidget(self.activityLabel)
        self.acttextLayout.addWidget(self.activityName)
        self.acttextLayout.addStretch()



        self.timesLabel = QLabel(" Aktivite Tekrarı :")

        self.timesNumber = QLineEdit()
        self.timesNumber.setText(self.doneTimes)
        self.timesNumber.setReadOnly(True)
        self.timesNumber.setMaximumWidth(30)
        self.upHorizontalLayout.addWidget(self.timesLabel)
        self.upHorizontalLayout.addWidget(self.timesNumber)
        self.upHorizontalLayout.addStretch()
        

        self.neccesaryCount = QLabel("Tahmin için gereken tekrar :")
        self.neccesaryCountEdit = QLineEdit()
        self.neccesaryCountEdit.setText(self.needToDo)
        self.neccesaryCountEdit.setMaximumWidth(30)
        self.neccesaryCountEdit.setReadOnly(True)
        self.mouseDoubleClickEvent = self.mouseDoubleClickEvent
        
        self.middleHoriziontalLayout.addWidget(self.neccesaryCount)
        self.middleHoriziontalLayout.addWidget(self.neccesaryCountEdit)
        self.middleHoriziontalLayout.addStretch()

        #Widget barındıran Layoutların ana layout'a eklenmesi
        self.mainVerticalLayout.addLayout(self.acttextLayout)        
        self.mainVerticalLayout.addLayout(self.upHorizontalLayout)
        self.mainVerticalLayout.addLayout(self.middleHoriziontalLayout)        
        
        self.setLayout(self.mainVerticalLayout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    obj = JobInfo("Basketbol",7,15)
    obj.show()
    sys.exit(app.exec_())
