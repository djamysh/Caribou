import sys
from progressBar import Ui_ProgressBar
from PyQt5 import QtWidgets,QtCore
import psutil

class ProgressBarClass(QtWidgets.QWidget,Ui_ProgressBar):
    def __init__(self,parent = None):
        super(ProgressBarClass,self).__init__(parent)
        self.setupUi(self)
        self.initUI()

        #self.threading = ThreadClass()
        #self.threading.start()
        #self.connect(self.ThreadClass,QtCore.pyqtSignal("cpu_value"),self.updateProgressBar)

    def initUI(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateProgressBar)
        self.timer.start(1000)        

    def updateProgressBar(self):
        val = psutil.cpu_percent(interval=1)
        self.progressBar.setValue(val)    

"""
class ThreadClass(QtCore.QThread):
    def __init__(self,parent=None):
        super(ThreadClass,self).__init__(parent)
    
    def run(self):
        while 1:
            val = getCPU_percent()
            self.emit(QtCore.pyqtSignal("cpu_value"),val)

    """
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    obj= ProgressBarClass()
    obj.show()
    app.exec_()
