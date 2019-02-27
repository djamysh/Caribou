from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class newTimeRange(QGroupBox):
    newRangeSignal = pyqtSignal(str)
    def __init__(self, *args, **kwargs):
        super(newTimeRange,self).__init__()
        self.initUI()

    def initUI(self):
        self.mainHorizontal = QHBoxLayout()
        
        self.VerticalStart = QVBoxLayout()
        self.horizontalStartInputField = QHBoxLayout()
        
        self.startLabel = QLabel("Başlangıç")
        self.startLabel.setAlignment(Qt.AlignHCenter)
        self.hourCombo1 = QComboBox()
        self.minuteCombo1 = QComboBox()
        self.horizontalStartInputField.addWidget(self.hourCombo1)
        self.horizontalStartInputField.addWidget(QLabel(":"))
        self.horizontalStartInputField.addWidget(self.minuteCombo1)
        self.VerticalStart.addWidget(self.startLabel)
        self.VerticalStart.addLayout(self.horizontalStartInputField)
        
        self.VerticalEnd = QVBoxLayout()
        self.horizontalEndInputField = QHBoxLayout()
        
        self.endLabel = QLabel("Bitiş")
        self.endLabel.setAlignment(Qt.AlignHCenter)
        self.hourCombo2 = QComboBox()
        self.minuteCombo2 = QComboBox()
        self.horizontalEndInputField.addWidget(self.hourCombo2)
        self.horizontalEndInputField.addWidget(QLabel(":"))
        self.horizontalEndInputField.addWidget(self.minuteCombo2)
        self.VerticalEnd.addWidget(self.endLabel)
        self.VerticalEnd.addLayout(self.horizontalEndInputField)
        
        for i in range(24):
            if i<10:
                element = "0"+str(i)
            else:
                element = str(i)
            self.hourCombo1.addItem(element,i)#element,index
            self.hourCombo2.addItem(element,i)#element,index

        for i in range(60):
            if i<10:
                element = "0"+str(i)
            else:
                element = str(i)
            self.minuteCombo1.addItem(element,i)#element,index
            self.minuteCombo2.addItem(element,i)#element,index


        self.mainHorizontal.addLayout(self.VerticalStart)
        self.mainHorizontal.addWidget(QLabel("--"))
        self.mainHorizontal.addLayout(self.VerticalEnd)

        self.mainHorizontal.setAlignment(Qt.AlignCenter)        


        self.okayButton = QPushButton("Tamam")
        self.okayButton.clicked.connect(self.okay)
        self.cancelButton = QPushButton("İptal")
        self.mainHorizontal.addWidget(self.okayButton)
        self.mainHorizontal.addWidget(self.cancelButton)

        self.setLayout(self.mainHorizontal)

    def adjustInput(self):
        h1,m1,h2,m2 = self.getInput()
        if len(h1)==1:
            h1 = "0"+h1
        if len(m1)==1:
            m1 = "0"+m1
        if len(h2)==1:
            h2 = "0"+h2
        if len(m2)==1:
            m2 = "0"+m2
        return h1+":"+m1+"-"+h2+":"+m2                    

    def getInput(self):
        
        h1 = str(self.hourCombo1.currentIndex())
        m1 = str(self.minuteCombo1.currentIndex())
        h2 = str(self.hourCombo2.currentIndex())
        m2 = str(self.minuteCombo2.currentIndex())
        return (h1,m1,h2,m2)
    def okay(self):
        self.newRangeSignal.emit(self.adjustInput())
        
    def cancel(self):
        self.newRangeSignal.emit(False)
    def cleanInputs(self):
        self.hourCombo1.setCurrentIndex(0)
        self.minuteCombo1.setCurrentIndex(0)

        self.hourCombo2.setCurrentIndex(0)
        self.minuteCombo2.setCurrentIndex(0)


class OtherWidget(QWidget):
    def __init__(self, parent=None):
        super(OtherWidget, self).__init__(parent)
        self.label = QLabel()
        lay = QVBoxLayout(self)
        lay.addWidget(self.label, alignment=Qt.AlignCenter)

    @pyqtSlot(str)
    def setText(self, text):
        self.label.setText(text)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    obj = newTimeRange()
    other = OtherWidget()
    obj.newRangeSignal.connect(other.setText)
    obj.show()
    other.show()

    sys.exit(app.exec_())
