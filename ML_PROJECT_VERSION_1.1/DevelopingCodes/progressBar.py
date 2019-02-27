from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import time
class PbWidget(QProgressBar):
    def __init__(self, parent=None, total=20):
        super(PbWidget, self).__init__()
        self.setMinimum(1)
        self.setMaximum(total)        
        self.setGeometry(QRect(10, 50, 371, 41))
        self.SS = """
        QProgressBar::chunk { 
            background:#4001b1;
            }  
        """#Kullanılmadı
        self._active = False
        

    def update_bar(self, to_add_number):
        while True:
            time.sleep(0.01)
            value = self.value() + to_add_number            
            self.setValue(value)
            qApp.processEvents()
            if (not self._active or value >= self.maximum()):                
                break
        self._active = False

    def closeEvent(self, event):
        self._active = False


class ProgressWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super(ProgressWidget,self).__init__()
        self.processText = "İşlemler\n{}".format("#"*24)
        self.setMinimumWidth(350)
        self.initUI()
    def initUI(self):
        self.mainVerticalLayout = QVBoxLayout()
        self.progressBar = PbWidget(total=100)
        self.proceses = QTextBrowser()
        self.procesesSS = """
            font-size:10px;
            font-style:Consolas;
            background-color:black;
            color:green;
        """
        self.proceses.setStyleSheet(self.procesesSS)
        self.proceses.setMaximumHeight(100)
        self.proceses.setText(self.processText)
        
        self.mainVerticalLayout.addWidget(self.progressBar)
        self.mainVerticalLayout.addWidget(self.proceses)
        self.setLayout(self.mainVerticalLayout)

    def addProgression(self,add,text):
        
        self.progressBar.update_bar(add)
        self.processText += "\n"+text
        self.proceses.setText(self.processText)



if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    obj = ProgressWidget()
    obj.show()
    sys.exit(app.exec_())