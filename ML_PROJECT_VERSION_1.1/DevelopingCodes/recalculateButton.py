from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class calculateButton(QPushButton):
    def __init__(self,connectionFunction,iconPath = False,*args,**kwargs):
        super(calculateButton,self).__init__()
        self.connectionFunction = connectionFunction
        self.clicked.connect(self.fadeAndFunctionality)
        self.setIconSize(QSize(32,32))
        if bool(iconPath):
            self.pixmap = QPixmap(iconPath)
            self.setIcon(QIcon(self.pixmap))
            
            #Gelen Icon boyutuna göre maksimum ve minimum boyutları ayarla
        
    def fade(self):
        self.setWindowOpacity(0.5)
        

    def unfade(self):
        self.setWindowOpacity(1)

    def fadeAndFunctionality(self):
        self.fade()
        self.connectionFunction()
        self.unfade()
    

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    function = lambda:print("Clicked")
    obj = calculateButton(function,iconPath="/home/wasptheslimy/Desktop/ML_Project_Version1.1/Kodlar/Images/calculator.png")
    obj.show()
    sys.exit(app.exec_())
