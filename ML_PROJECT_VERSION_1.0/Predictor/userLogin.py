#Arayüz Tasarım modülleri
from PyQt5.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QPushButton,QLineEdit,QLabel,QRadioButton,QGraphicsDropShadowEffect,QApplication
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap,QColor
#Kendi implementasyonumuz olan modüller
from sqliteModule import sql_functions 
from dirPath import get_dir_path
from userDatabaseConfiguration import usersConf,tableCheck
#Diğer modüller
from passlib.hash import sha256_crypt
import sys
import os

class userLoginForm(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.setWindowTitle("Kullanıcı Girişi")
        self.dir_path = get_dir_path()
        self.userDatabaseControl()
        self.userDB = sql_functions("{}Databases/users.db".format(self.dir_path))#Kullanıcı veritabanı ile bağlantının kurulması
        self.setMaximumSize(356,206)#Ekran boyutları
        self.initUI()#Arayüz tasarım kodlarının çalıştırılması


    def initUI(self):

        #Layout'ların tanımlanması
        self.mainVerticalLayout = QVBoxLayout()
        self.headerLayout = QHBoxLayout()
        self.upLayout = QHBoxLayout()
        self.middleLayout = QHBoxLayout()
        self.downLayout = QHBoxLayout()
        self.notificationLayout = QHBoxLayout()


        # Widgetlerin tanımlanması,tasarımının yapılması ve Layout'lara yüklenmesi.

        self.header = QLabel()
        self.header.setText("Kullanıcı Girişi")
        self.header.setStyleSheet(
        """
        font-family:Courier;
        font-size:32px;
        color:#003366;
        border-left: 4px solid #221354;

        padding:3px;
        background-color: lightgrey;
        """)
        self.headerLayout.addStretch()
        self.headerLayout.addWidget(self.header)
        self.headerLayout.addStretch()


        self.userNameLabel = QLabel()
        self.userNameLabel.setText("Kullanıcı Adı : ")
        self.userNameLabel.setStyleSheet("""
        border-right:4px solid #221354;          
        font-family:Verdana;
        font-size:14px;
        color:#201A1E;
        """) 
        self.userNameLineEdit = QLineEdit()
        self.userNameLineEdit.setMaximumWidth(150)
        
        self.upLayout.addStretch()
        self.upLayout.addWidget(self.userNameLabel)
        self.upLayout.addWidget(self.userNameLineEdit)
        self.upLayout.addStretch()

        self.passwordLabel = QLabel()
        self.passwordLabel.setText("                 Şifre : ")
        self.passwordLabel.setStyleSheet("""
        font-family:Verdana;
        font-size:14px;
        color:#201A1E;
        """)  
        self.passwordLineEdit = QLineEdit()
        self.passwordLineEdit.setMaximumWidth(150)
        self.readablePassword = QRadioButton()
        
        self.timer = QTimer()
        self.timer.timeout.connect(self._update)
        self.timer.start(1000)
        

        self.middleLayout.addStretch()
        self.middleLayout.addWidget(self.passwordLabel)
        self.middleLayout.addWidget(self.passwordLineEdit)
        self.middleLayout.addWidget(self.readablePassword)
        self.middleLayout.addStretch()


        self.registerbutton = QPushButton("Kayıt")
        self.registerbutton.setStyleSheet("""
        color:  #80004d;
        background-color:#aaaaaa;
        font-weight: 650 ;
        font-style:Verdana;       
        """)
        shadow = QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3)
        self.registerbutton.setGraphicsEffect(shadow)        
        self.registerbutton.clicked.connect(self.register)#Kayıt sayfasına yönlendirecek fonksiyonun çağrılması

        self.loginbutton = QPushButton("Giriş")
        self.loginbutton.setStyleSheet("""
        color: #008080;
        background-color:#aaaaaa;
        font-weight: 650 ;
        font-style:Verdana;       
        """)
        shadow = QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3)
        self.loginbutton.setGraphicsEffect(shadow)
        self.loginbutton.clicked.connect(self.login)#Veritabanında bilgi kontrolünü yapacak fonksiyonun çağrılması
        
        
        self.downLayout.addStretch()
        self.downLayout.addWidget(self.loginbutton)
        self.downLayout.addWidget(self.registerbutton)
        
        self.registeredNotificationLabel = QLabel()
        self.registeredNotificationImage = QLabel()

        self.notificationLayout.addStretch()
        self.notificationLayout.addWidget(self.registeredNotificationImage)
        self.notificationLayout.addWidget(self.registeredNotificationLabel)
        self.notificationLayout.addStretch()



        #İşlenen Layout'ların ana Layout'a eklenmesi
        self.mainVerticalLayout.addStretch()
        self.mainVerticalLayout.addLayout(self.headerLayout)
        self.mainVerticalLayout.addLayout(self.upLayout)
        self.mainVerticalLayout.addLayout(self.middleLayout)
        self.mainVerticalLayout.addLayout(self.downLayout)
        self.mainVerticalLayout.addLayout(self.notificationLayout)
        self.mainVerticalLayout.addStretch()
        

        self.setAutoFillBackground(True)        
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(240,250,253))
        self.setPalette(p)

        self.setLayout(self.mainVerticalLayout)

    def userDatabaseControl(self):
        condition1 = os.path.isdir("{}Databases/".format(self.dir_path))#Dizinin kontrolü
        condition2 = os.path.exists("{}Databases/users.db".format(self.dir_path))#Veritabanının kontrolü
        condition3 = tableCheck("{}Databases/users.db".format(self.dir_path),"Users")#Tablonun varlığının kontrolü

        if not condition1:
            #Dizin kontrol ==> yanlış
            os.mkdir("{}Databases/".format(self.dir_path))

        elif condition2:
            usersConf()
        
        elif condition3:
            os.remove("{}Databases/users.db".format(self.dir_path))
            usersConf()

    def _update(self):#Şifrenenin görünürlüğünü anlık olarak radiobutton'a bakarak kontrol eder ve değiştiririr.
        if self.readablePassword.isChecked():
            self.passwordLineEdit.setEchoMode(False)
        else:
            self.passwordLineEdit.setEchoMode(QLineEdit.Password)

        self.setLayout(self.mainVerticalLayout)


                
    def register(self):#Kayıt sayfasına yönlendirir.
        from registrationPage import registrationForm#Eğer en başta belirtilir ise import hatası verecektir

        self.close()
        self.openWindow = registrationForm()
        self.openWindow.show()

    def login(self):#Giriş yapar
        nickname = self.userNameLineEdit.text()
        password = self.passwordLineEdit.text()

        nicknameExistance = nickname in [tup[0] for tup in self.userDB.get_column_by_name("users","Username")]#kullanıcı isminin veri tabanında varlığını boolean veri tipinde değişkene atar
        userData = self.userDB.get_row("users","Username",nickname)
        
        if nicknameExistance :#Kullanıcı imi olursa bu bölge çalışır
            hashedPassword = userData[5]#SHA256 ile şifrelenmiş şifre bilgisi

            if sha256_crypt.verify(password,hashedPassword):#Eğer şifre bilgisi ile girilen şifre doğrulanırsa bu bölge çalışır.
                self.registeredNotificationLabel.setText("Hoşgeldin {} ".format(userData[3]))

                self.registeredNotificationImage.setPixmap(QPixmap("{}Images/tickIconAdjusted.png".format(self.dir_path)))
                QTimer.singleShot(1800,lambda:self.registeredNotificationLabel.setText(""))
                QTimer.singleShot(1800,lambda:self.registeredNotificationImage.setPixmap(QPixmap()))

                userIndex = [tup[0] for tup in self.userDB.get_column_by_name("users","Username")].index(nickname)
                from interface import mainScreen
                self.openWindow = mainScreen(userIndex)#Ana ekrana giriş yapılır
                self.openWindow.show()
                self.close()


            else:#Hatalı şifre durumunda çalışır
                self.readablePassword.setChecked(True)
                self.passwordLineEdit.setText("Şifre yanlış girildi.Tekrar deneyiniz.")
        else:#Kullanıcı adı geçersiz ise çalışır
            self.userNameLineEdit.setText("Geçersiz kullanıcı adı.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    obj = userLoginForm()
    obj.show()
    sys.exit(app.exec_())
