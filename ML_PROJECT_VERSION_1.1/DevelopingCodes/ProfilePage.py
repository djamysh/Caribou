from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from sqliteModule import sql_functions
from dirPath import get_dir_path
import sys
import os
import shutil
from PIL import Image

from passlib.hash import sha256_crypt
from specializedWidgets import specializedQLabel,specializedQLineEdit,specializedQPushButton

#Şifre değiştir tasarla#Basit tasarım yapıldı
#Değişiklik Kaydetme butonunu tasarla ve devreleri kur#Kurludu
#Aktivite bilgileri ağacı#Bu özel bir sayfa oluşturacak
#Kullanıcı resmini daha hoş bir hale getir#+
#Arayüz tasarımını yap#+
#Bazı şeyler geliştirilmeyi bekliyor.basit dizayn böyle işte.

class Profile(QWidget):
    def __init__(self,UserIndex, *args, **kwargs):
        super().__init__()
        self.path = get_dir_path()
        self.UserIndex = UserIndex
        __usersDB = sql_functions("{}Databases/users.db".format(self.path))
        __userData = __usersDB.get_row_with_ID("Users",self.UserIndex)
        __usersDB.disconnect_from_database()
        self.installEventFilter(self)
        self.setWindowTitle("Profil Sayfası")
        self.setMaximumWidth(557)
        self.registrationDate = __userData[0]
        self.email = __userData[1]
        self.nickname = __userData[2]
        self.name = __userData[3]
        self.surname = __userData[4]
        self.__passwordHashed = __userData[5]#Gizlilik amaçlı

        self.formatImagePath = "{}Images/userImages/genderlessUser.png".format(self.path)
        self.userImagePath = "{}Images/userImages/user{}.png".format(self.path,hex(self.UserIndex)[2:])
        self.psudoImagePath = ""
        self.setStyleSheet("""
        background-color: #C6E2FF;
        """)
        self.initUI()

    def initUI(self):
        self.mainVerticalLayout = QVBoxLayout()

        self.TopHorizontalLayout = QHBoxLayout()
        self.upLeftVerticalLayout = QVBoxLayout()
        self.upRightVerticalLayout = QVBoxLayout()
        self.downRightVerticalLayout = QVBoxLayout()



        self.lineWidthTimer = QTimer()
        self.lineWidthTimer.timeout.connect(self._lineWidthUpdater)
        self.lineWidthTimer.start(0)

        ####################################Right Vertical Layout
        self.emailLayout = QHBoxLayout()
        self.emailLine = specializedQLineEdit(text = self.email)
        self.emailLabel = specializedQLabel(self.emailLine,text="E-Posta",max_Width=100)
        self.emailLayout.addWidget(self.emailLabel)
        self.emailLayout.addWidget(self.emailLine)


        self.nicknameLayout = QHBoxLayout()
        self.nicknameLine = specializedQLineEdit(text= self.nickname)
        self.nicknameLabel = specializedQLabel(self.nicknameLine,text="Kullanıcı adı ",max_Width=100)
        self.nicknameLayout.addWidget(self.nicknameLabel)
        self.nicknameLayout.addWidget(self.nicknameLine)

        self.nameLayout = QHBoxLayout()
        self.nameLine = specializedQLineEdit(text= self.name)
        self.nameLabel = specializedQLabel(self.nameLine,text="İsim ",max_Width=100)
        self.nameLayout.addWidget(self.nameLabel)
        self.nameLayout.addWidget(self.nameLine)
        
        self.surnameLayout = QHBoxLayout()
        self.surnameLine = specializedQLineEdit(text = self.surname)
        self.surnameLabel = specializedQLabel(self.surnameLine,text="Soyisim ",max_Width=100)
        self.surnameLayout.addWidget(self.surnameLabel)
        self.surnameLayout.addWidget(self.surnameLine)



        self.upRightVerticalLayout.addLayout(self.emailLayout)
        self.upRightVerticalLayout.addLayout(self.nicknameLayout)
        self.upRightVerticalLayout.addLayout(self.nameLayout)
        self.upRightVerticalLayout.addLayout(self.surnameLayout)
        self.upRightVerticalLayout.addStretch()

        ####################################Right Vertical Layout

        ####################################Left Vertical Layout
        if os.path.isfile(self.userImagePath):
            self.imagePixmap = QPixmap(self.userImagePath)
        else:
            self.imagePixmap = QPixmap(self.formatImagePath)

        self.imagePixmap = self.imagePixmap.scaled(128,128,Qt.KeepAspectRatio)
        self.image = QLabel()
        self.image.setPixmap(self.imagePixmap)

        self.image.setFrameStyle(6)
        self.image.setStyleSheet("""
        border: 3px solid #4B666E;
        background-color : #EEFDF5;
        padding:12px;
        """)

        self.addImageLayout = QHBoxLayout()
        self.addImageButton = QPushButton("Profil Resmini Değiştir")
        self.addImageButton.clicked.connect(self.addImage)
        #self.chageImagePixmap = QPixmap("{}Images/changeImage.png".format(self.path))
        #self.changeImagePixmap = self.chageImagePixmap.scaled(32,32,Qt.KeepAspectRatio)
        #self.addImageButton = specializedQPushButton(self.chageImagePixmap,self.addImage)


        self.addImageLayout.addWidget(self.addImageButton)
        self.addImageLayout.addStretch()
        

        self.upLeftVerticalLayout.addWidget(self.image)
        self.upLeftVerticalLayout.addLayout(self.addImageLayout)
        self.upLeftVerticalLayout.addStretch()
        ####################################Left Vertical Layout
        
        #################################################################################33
        self.adjustHorizontalityChangePassword = QHBoxLayout()

        self.changePasswordButton = QPushButton("Şifreyi Değiştir")
        self.changePasswordButton.setMinimumWidth(120)
        self.changePasswordButton.clicked.connect(self.changePasswordFunctionVisiualSide)
        
        self.oldPasswordLayout = QHBoxLayout()
        self.oldPassword = QLineEdit()
        self.oldPassword.setHidden(True)

        self.readablePassword = QRadioButton()
        self.readablePassword.setHidden(True)

        self.timerPasswordReadability = QTimer()
        self.timerPasswordReadability.timeout.connect(self._passwordReadablility)
        self.timerPasswordReadability.start(1000)

        self.oldPasswordLayout.addWidget(self.oldPassword)
        self.oldPasswordLayout.addWidget(self.readablePassword)



        self.newPassword = QLineEdit()
        self.newPassword.setHidden(True)
        self.newPassword.setEchoMode(QLineEdit.Password)

        self.newPasswordVerify = QLineEdit()
        self.newPasswordVerify.setHidden(True)
        self.newPasswordVerify.setEchoMode(QLineEdit.Password)

        self.changePasswordResponseLayout = QHBoxLayout()

        self.changeButton = QPushButton("Değiştir")
        self.changeButton.clicked.connect(self.changePasswordFunctionDatabaseSide)
        self.changeButton.setHidden(True)

        self.cancelButton = QPushButton("İptal")
        self.cancelButton.clicked.connect(self.changePasswordOpTerminate)
        self.cancelButton.setHidden(True)
        
        self.changePasswordResponseLayout.addWidget(self.cancelButton)
        self.changePasswordResponseLayout.addWidget(self.changeButton)


        self.downRightVerticalLayout.addWidget(self.changePasswordButton)
        self.downRightVerticalLayout.addLayout(self.oldPasswordLayout)
        self.downRightVerticalLayout.addWidget(self.newPassword)
        self.downRightVerticalLayout.addWidget(self.newPasswordVerify)
        self.downRightVerticalLayout.addLayout(self.changePasswordResponseLayout)

        self.adjustHorizontalityChangePassword.addStretch()
        self.adjustHorizontalityChangePassword.addLayout(self.downRightVerticalLayout)
        self.upRightVerticalLayout.addLayout(self.adjustHorizontalityChangePassword)

        #####################################################      

        self.mouseDoubleClickEvent = self.mouseDoubleClickEvent
      
        ####################################TOPLayout Staff
        self.TopHorizontalLayout.addLayout(self.upLeftVerticalLayout)
        self.TopHorizontalLayout.addLayout(self.upRightVerticalLayout)
        ####################################TOPLayout Staff



        #####################################################

        self.endLayout = QHBoxLayout()

        self.saveButton = QPushButton("Kaydet")
        self.saveButton.setMaximumWidth(120)
        self.saveButton.setMinimumWidth(120)
        self.saveButton.clicked.connect(self.saveChanges)
        self.backToMainButton = QPushButton("Geri Dön")
        self.backToMainButton.clicked.connect(self.backToMain)
        self.logoutButton = QPushButton("Çıkış Yap")
        self.logoutButton.clicked.connect(self.logout)

        self.endLayout.addWidget(self.logoutButton)
        self.endLayout.addWidget(self.backToMainButton)
        self.endLayout.addStretch()
        self.endLayout.addWidget(self.saveButton)
        #####################################################

        #####################################################
        self.notificationLayout = QHBoxLayout()
        self.NotificationLabel = QLabel()
        self.NotificationImage = QLabel()

        self.notificationLayout.addStretch()
        self.notificationLayout.addWidget(self.NotificationImage)
        self.notificationLayout.addWidget(self.NotificationLabel)
        #####################################################


        self.mainVerticalLayout.addLayout(self.TopHorizontalLayout)
        #self.mainVerticalLayout.addLayout(self.BottomHorizontalLayout)
        self.mainVerticalLayout.addLayout(self.endLayout)
        self.mainVerticalLayout.addLayout(self.notificationLayout)
        self.setLayout(self.mainVerticalLayout)
        ####################################Layout Staff

    def notify(self,message,pixmap = False,styleSheet = False,delay = 3,situation = "positive"):
            self.positiveNotifyStyleSheet = """
                font-family:Courier;
                font-size:14px;
                font-weight:650;
                color :#5A2C63;
                background-color:#C4FFC1;
                border-left:4px solid  	#35632c;
                padding : 4px;
                """
            self.positivePixmap = QPixmap("{}Images/tickIconAdjusted.png".format(self.path)) 
            self.negativeNotifyStyleSheet = """
                font-family:Courier;
                font-size:14px;
                font-weight:650;
                color:#d22323;
                background-color:#f4919f;
                border-left:8px solid  #4F646B;
                padding:6px;  
            """
            self.negativePixmap = QPixmap("{}Images/error.png".format(self.path))

            if not bool(styleSheet):
                if situation == "positive":
                    pixmap = self.positivePixmap;styleSheet = self.positiveNotifyStyleSheet

                elif situation == "negative":
                    pixmap = self.negativePixmap;styleSheet = self.negativeNotifyStyleSheet

                else:
                    return 0
                    #Error

            else:
                if type(pixmap) == type(self.positivePixmap) and not(pixmap.isNull) and isinstance(styleSheet,str):
                    pixmap = pixmap;styleSheet = styleSheet
                else:
                    return 0
                    #error

            
            
            self.NotificationImage.setPixmap(pixmap)
            self.NotificationLabel.setText(message)
            self.NotificationLabel.setStyleSheet(styleSheet)

            QTimer.singleShot(delay*1000,lambda:self.NotificationLabel.setText(""))
            QTimer.singleShot(delay*1000,lambda:self.NotificationLabel.setStyleSheet(""))
            QTimer.singleShot(delay*1000,lambda:self.NotificationImage.setPixmap(QPixmap()))

    def addImage(self):
        fileName = QFileDialog.getOpenFileName()
        imagePath = fileName[0]
        pixmap = QPixmap(imagePath)
        if not pixmap.isNull():
            pixmap = pixmap.scaled(196,196,Qt.KeepAspectRatio)
            self.image.setPixmap(pixmap)
            self.psudoImagePath = imagePath

        else:
            self.notify("Geçersiz format.",situation="negative")
    def changePasswordFunctionDatabaseSide(self):
        oldPass = self.oldPassword.text()
        if sha256_crypt.verify(oldPass,self.__passwordHashed):
            print("[+] old password enterance verified")
            if self.newPassword.text() == self.newPasswordVerify.text():
                print("[+] new password entrance verified")
                newPass = self.newPassword.text()
                self.__passwordHashed = sha256_crypt.encrypt(newPass)
                print("[I] hashed new password : ",self.__passwordHashed)
                __usersDB = sql_functions("{}Databases/users.db".format(self.path))
                __usersDB.update_data("Users","Password","Date",self.__passwordHashed,self.registrationDate)
                self.notify("Şifre başarı ile değiştirildi.",situation="positive")
                self.changePasswordFunctionVisiualSide(reverse=True)
                self.cleanPasswordChangeLineEdits()
                
            else:
                self.notify("Başarısız şifre doğrulama.",situation="negative")
        else:
            self.notify("Yanlış şifre.Tekrar deneyiniz.",situation="negative")

        
    def cleanPasswordChangeLineEdits(self):
        self.oldPassword.clear()
        self.newPassword.clear()
        self.newPasswordVerify.clear()

    def changePasswordFunctionVisiualSide(self,reverse = False):
        if reverse:
            manager = True
        else:
            manager = False
        self.oldPassword.setHidden(manager or False)
        self.readablePassword.setHidden(manager or False)
        self.newPassword.setHidden(manager or False)
        self.newPasswordVerify.setHidden(manager or False)
        self.cancelButton.setHidden(manager or False)
        self.changeButton.setHidden(manager or False)

    def saveChanges(self):
        change = False
        email = self.emailLine.text()
        nickname = self.nicknameLine.text()
        name = self.nameLine.text()
        surname = self.surnameLine.text()
        if  (email != self.email or nickname != self.nickname or name != self.name or surname != self.surname ):
            if ((email and nickname and name and surname) != ""):
                if "@" in email:
                    print("we are in")
                    __usersDB = sql_functions("{}Databases/users.db".format(self.path))
                    __usersDB.update_data("Users","Email","Date",email,self.registrationDate)
                    __usersDB.update_data("Users","Username","Date",nickname,self.registrationDate)
                    __usersDB.update_data("Users","Name","Date",name,self.registrationDate)
                    __usersDB.update_data("Users","Surname","Date",surname,self.registrationDate)
                    self.email = email;self.nickname = name;self.name = name;self.surname = surname

                    change = True
                    

                else:
                    self.notify("Geçersiz e-posta adresi.",situation="negative")
            else:
                self.notify("Geçersiz girdi.",situation="negative")
        
        if self.psudoImagePath != "":
            image = Image.open(self.psudoImagePath)
            image.save(self.userImagePath)
            self.psudoImagePath = ""
            change = True

        if change:
            self.notify("Değişiklikler başarı ile kaydedildi.",situation="positive")


    
    def backToMain(self):
        # Burada yönlediriciyi al ve geri yönlendirme yap.
        # Yönlendirici değişkenini bu sınıfın parametrelerinde al
        from interface import mainScreen
        self.redirect = mainScreen(self.UserIndex)
        self.redirect.show()
        self.close()
    
    def logout(self):
        #Kullanıcıya giriş ekranına mı yoksa temelli sistemi sonlandırmayı mı istediğini sor
        from userLogin import userLoginForm

        self.redirect = userLoginForm()
        self.redirect.show()
        self.close()
        

        
    def changePasswordOpTerminate(self):
        self.cleanPasswordChangeLineEdits()
        self.changePasswordFunctionVisiualSide(reverse=True)
        

    def _passwordReadablility(self):
        if self.readablePassword.isChecked():
            self.oldPassword.setEchoMode(False)
        else:
            self.oldPassword.setEchoMode(QLineEdit.Password)

    def _lineWidthUpdater(self):
        max_Width = 0
        for stage in range(2):
            for obj in [self.emailLine,self.nicknameLine,self.nameLine,self.surnameLine]:
                if not stage:#Stage == 0 durumu
                    width = len(str(obj.text()))*10
                    if width > max_Width:
                        max_Width = width
                else : 
                    obj.setMaximumWidth(max_Width)
                    obj.setMinimumWidth(max_Width)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    obj = Profile(0)
    obj.show()
    sys.exit(app.exec_())