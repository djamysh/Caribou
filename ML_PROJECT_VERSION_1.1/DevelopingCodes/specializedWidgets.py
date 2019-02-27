from PyQt5.QtWidgets import QLabel,QLineEdit,QPushButton
from PyQt5.QtCore import QTimer,Qt,QSize
from PyQt5.QtGui import QPainter


class specializedQLabel(QLabel):
    def __init__(self,specifyObject,text = "",max_Width = False,min_Width = False,*args, **kwargs):
        super(specializedQLabel,self).__init__()
        self.setText(text)
        if max_Width:
            self.setMaximumWidth(max_Width)
        if min_Width:
            self.setMinimumWidth(min_Width)
        self.specifyObject = specifyObject
        self.normalStyleSheet ="""
        border: 0px solid white;
        border-left: 2px solid  #542913;
        background-color : 	#ffe3c6;
        color : #171436;
        font-size : 15px;
        font-family : "Palatino Linotype", "Book Antiqua", Palatino, serif ;

        """
        self.setStyleSheet(self.normalStyleSheet)

    def enterEvent(self,event):
        self.specifyObject.showerEntered()
        self.setStyleSheet(self.normalStyleSheet+"color:#212ed4;")
        QTimer.singleShot(250,lambda:self.setStyleSheet(self.normalStyleSheet))

    def mouseDoubleClickEvent(self,event):
        self.specifyObject.changeSituation()

class specializedQLineEdit(QLineEdit):
    def __init__(self,text = "" ,max_Width = False,min_Width = False,*args, **kwargs):
        super(specializedQLineEdit,self).__init__()
        self.readOnlySituation = True
        if max_Width:
            self.setMaximumWidth(max_Width)
        if min_Width:
            self.setMinimumWidth(min_Width)        
        self.setText(text)
        self.setReadOnly(self.readOnlySituation)
        self.normalStyleSheet = """
        border : 0px solid red;
        border-bottom : 3px solid  	#079693 ;
        border-top : 3px solid  	#079693;
        border-radius : 3px;
        background-color : 	 	#ede3fb;
        font-family:courier;
        font-size : 16px;
        font-weight : 650;
        color : #4b0796;
        """
        self.dblClickStyleSheet = """
            border : 0px solid white;
            border-bottom : 3px solid #07964b ;
            border-radius : 3px;
            background-color : 	#C6E2FF;
            font-family:courier;
            font-size : 16px;
            font-weight : 650;
            color : #960752;
            """
        
        self.setStyleSheet(self.normalStyleSheet)
    
    def changeSituation(self):
        self.readOnlySituation = not self.readOnlySituation
        if not self.readOnlySituation:
            self.setStyleSheet(self.dblClickStyleSheet)
        
        else: 
            self.setStyleSheet(self.normalStyleSheet)

        self.setReadOnly(self.readOnlySituation)


    def showerEntered(self):
        if self.readOnlySituation:
            oldStyleSheet = self.normalStyleSheet
        else:
            oldStyleSheet = self.dblClickStyleSheet
            
        self.setStyleSheet(oldStyleSheet+"font-weight:bold;color : #21D4C7;")
        QTimer.singleShot(250,lambda:self.setStyleSheet(oldStyleSheet))


    def mouseDoubleClickEvent(self,event):
        self.changeSituation()

    def keyPressEvent(self,event):
        if event.key() == Qt.Key_Return:#16777220:#enter butonunun anahtar kodu
            self.changeSituation()
        else:
            QLineEdit.keyPressEvent(self,event)# source : https://stackoverflow.com/questions/48978661/pyqt-dual-purpose-enter-key-press
            #Tarih : 15 Ocak 2019

class specializedQPushButton(QPushButton):
    def __init__(self,pixmap,connectionFunction, *args, **kwargs):
        super(specializedQPushButton,self).__init__()
        self.pixmap = pixmap
        self.connectionFunction = connectionFunction

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(event.rect(), self.pixmap)

    def mouseDoubleClickEvent(self,event):
        self.connectionFunction()

    def sizeHint(self):
        return QSize(64,64)