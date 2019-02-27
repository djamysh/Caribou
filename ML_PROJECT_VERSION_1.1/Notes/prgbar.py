class Crono(QtCore.QThread):
    tick = QtCore.pyqtSignal(int, name="changed") #New style signal

    def __init__(self, parent):
        QtCore.QThread.__init__(self,parent)

    def checkStatus(self):
        for x in range(1,101):
            self.tick.emit(x)                     
            time.sleep(1)

class WTrainning(wMeta.WMeta, QtGui.QWidget):

    def __init__(self):
        super(WTrainning, self).__init__()
        self.crono = Crono()

    def createUI(self):
        #Create GUI stuff here

        #Connect signal of self.crono to a slot of self.progressBar
        self.crono.tick.connect(self.progressBar.setValue)
if __name__ == "__main__":
    pass