#Modüllerin yüklenmesi
#Arayüz modülleri
from PyQt5.QtWidgets import QWidget,QHBoxLayout,QVBoxLayout,QLineEdit,QLabel,QPushButton,QRadioButton,QGraphicsDropShadowEffect
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap,QColor
#Kendi implementasyonumuz olan modüller
from dirPath import get_dir_path
from sqliteModule import sql_functions 
#diğer modüller
from passlib.hash import sha256_crypt
import sys
import datetime
from time import sleep

class registrationForm(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.dir_path = get_dir_path()# Ana kod dizinin bulunması
        self.userDB = sql_functions("{}Databases/users.db".format(self.dir_path))# Kullanıcı veritabanına bağlanılır
        self.setWindowTitle("Kayıt Formu")# Pencere başlığı
        # Ekran boyutları
        self.setMinimumSize(343,316)
        self.setMaximumSize(343,316)

        self.initUI()# Arayüz kodlarının çalıştırılması

    def initUI(self):

        # Layout'ların tanımlanması
        self.mainVerticalLayout = QVBoxLayout()
        self.headerLayout = QHBoxLayout()
        self.emailLayout = QHBoxLayout()
        self.nicknameLayout = QHBoxLayout()
        self.nameLayout = QHBoxLayout()
        self.surnameLayout = QHBoxLayout()
        self.passwordLayout = QHBoxLayout()
        self.downLayout = QHBoxLayout()
        self.notificationLayout = QHBoxLayout()

        
        shadow = QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3)#Gölge efekti
        
        #Widget'lerin tanımlanması,tasarlanması ve oluşturulan layout'lara eklenemesi

        self.header = QLabel()
        self.header.setText(" Kayıt Formu ")
        self.header.setStyleSheet("""
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

        
        self.emailLabel = QLabel()
        self.emailLabel.setText("E-Posta Adresi : ")
        self.emailLabel.setStyleSheet("""
        font-family:Verdana;
        font-size:14px;
        color:#201A1E;
        """)  
        self.emailLineEdit = QLineEdit()
        self.emailLineEdit.setMaximumWidth(150)


        self.emailLayout.addStretch()
        self.emailLayout.addWidget(self.emailLabel)
        self.emailLayout.addWidget(self.emailLineEdit)
        self.emailLayout.addStretch()


        self.nicknameLabel = QLabel()
        self.nicknameLabel.setText("    Kullanıcı Adı : ")
        self.nicknameLabel.setStyleSheet("""
        font-family:Verdana;
        font-size:14px;
        color:#201A1E;
        """)  
        self.nicknameLineEdit = QLineEdit()
        self.nicknameLineEdit.setMaximumWidth(150)

        self.nicknameLayout.addStretch()
        self.nicknameLayout.addWidget(self.nicknameLabel)
        self.nicknameLayout.addWidget(self.nicknameLineEdit)
        self.nicknameLayout.addStretch()
        

        self.nameLabel = QLabel()
        self.nameLabel.setText("                 İsim : ")
        self.nameLabel.setStyleSheet("""
        font-family:Verdana;
        font-size:14px;
        color:#201A1E;
        """)  
        self.nameLineEdit = QLineEdit()
        self.nameLineEdit.setMaximumWidth(150)

        self.nameLayout.addStretch()
        self.nameLayout.addWidget(self.nameLabel)
        self.nameLayout.addWidget(self.nameLineEdit)
        self.nameLayout.addStretch()



        self.surnameLabel = QLabel()
        self.surnameLabel.setText("            Soyisim : ")
        self.surnameLabel.setStyleSheet("""
        font-family:Verdana;
        font-size:14px;
        color:#201A1E;
        """)  
        self.surnameLineEdit = QLineEdit()

        self.surnameLineEdit.setMaximumWidth(150)        
        

        self.surnameLayout.addStretch()
        self.surnameLayout.addWidget(self.surnameLabel)
        self.surnameLayout.addWidget(self.surnameLineEdit)
        self.surnameLayout.addStretch()


        self.passwordLabel = QLabel()
        self.passwordLabel.setText("                       Şifre : ") 
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
        

        self.passwordLayout.addStretch()
        self.passwordLayout.addWidget(self.passwordLabel)
        self.passwordLayout.addWidget(self.passwordLineEdit)
        self.passwordLayout.addWidget(self.readablePassword)
        self.passwordLayout.addStretch()


        self.registerbutton = QPushButton("Kayıt")
        self.registerbutton.setStyleSheet("""
        color:  #80004d;
        background-color:#aaaaaa;
        font-weight: 650 ;
        font-style:Verdana;       
        """)
        self.registerbutton.setGraphicsEffect(shadow)        
        self.registerbutton.clicked.connect(self.register)# Bilgileri veritabanına yükleyecek fonksiyonun çağrılması


        self.backtoLoginButton = QPushButton("\u21A4 Geri dön")
        self.backtoLoginButton.setStyleSheet("""
        color: #008080;
        background-color:#aaaaaa;
        font-weight: 650 ;
        font-style:Verdana;       
        """)
        self.backtoLoginButton.setGraphicsEffect(shadow)
        self.backtoLoginButton.clicked.connect(self.backLogin)# Giriş ekranına yönlendiren fonksiyonun çağrılması
        

        self.downLayout.addWidget(self.backtoLoginButton)
        self.downLayout.addStretch()
        self.downLayout.addWidget(self.registerbutton)

        self.registeredNotificationLabel = QLabel()
        self.registeredNotificationImage = QLabel()

        self.notificationLayout.addStretch()
        self.notificationLayout.addWidget(self.registeredNotificationImage)
        self.notificationLayout.addWidget(self.registeredNotificationLabel)


        # Oluşturlan Layout'ların ana Layout'a eklenmesi
        self.mainVerticalLayout.addStretch()
        self.mainVerticalLayout.addLayout(self.headerLayout)
        self.mainVerticalLayout.addLayout(self.emailLayout)
        self.mainVerticalLayout.addLayout(self.nicknameLayout)
        self.mainVerticalLayout.addLayout(self.nameLayout)
        self.mainVerticalLayout.addLayout(self.surnameLayout)
        self.mainVerticalLayout.addLayout(self.passwordLayout)
        self.mainVerticalLayout.addLayout(self.downLayout)
        self.mainVerticalLayout.addLayout(self.notificationLayout)
        self.mainVerticalLayout.addStretch()
        self.setAutoFillBackground(True)        
        
        
        #Arka plan rengi
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(240,250,253))
        self.setPalette(p)

        self.setLayout(self.mainVerticalLayout)
        
        
        self.setLayout(self.mainVerticalLayout)#Ana layout'un belirtilmesi

    def _update(self):#Şifrenin okunurluğunu anlık olarak RadioButton'a bakarak belirleyen fonksiyon
        if self.readablePassword.isChecked():#Şifrenin okunamaması için
            self.passwordLineEdit.setEchoMode(False)
        else:
            self.passwordLineEdit.setEchoMode(QLineEdit.Password)

                
    def register(self):#Girilen bilgilerin veritabanına kayıt edilmesi
        email = self.emailLineEdit.text()
        nickname = self.nicknameLineEdit.text()
        name = self.nameLineEdit.text()
        surname = self.surnameLineEdit.text()
        password = self.passwordLineEdit.text()
        password = sha256_crypt.encrypt(password)#Girilen şifrenin SHA256 ile şifrelenmesi

        date = str(datetime.datetime.now())
        #Hataların handle edilmesi ve kullanıcıya hata bilgisinin döndürülmesi
        if nickname in [tup[0] for tup in self.userDB.get_column_by_name("users","Username")]:
            self.nicknameLineEdit.setText("Girilen kullanıcı adı daha önce kullanılmıştır.Yeni bir kullanıcı adı giriniz .")

        elif email in [tup[0] for tup in self.userDB.get_column_by_name("users","Email")] :
            self.emailLineEdit.setText("Girilen E-Posta adresi daha önce kayıt olmuştur.Yeni bir E-Posta adresi giriniz . ")
        
        elif not("@" in email):
            self.emailLineEdit.setText("Geçersiz E-Posta adresi ...")

        elif len(nickname) == 0:
            self.nameLineEdit.setText("Lütfen bir kullancı adı giriniz .")        

        elif len(surname) == 0:
            self.nameLineEdit.setText("Lütfen isminizi giriniz .")

        elif len(name) == 0:
            self.nameLineEdit.setText("Lütfen isminizi giriniz .")
        elif len(password) == 0:
            self.passwordLineEdit.setText("Lütfen bir şifre giriniz .")
        else:#Veri girişi hatasız ise bu bölüm çalışır
            self.userDB.insert_data("users",date,email,nickname,name,surname,password)#Kullanıcı Veritabanına bilgi akışı
            userIndex = [tup[0] for tup in self.userDB.get_column_by_name("users","Username")].index(nickname)#Kullanıcının, kayıt olan kaçıncı kullanıcı olduğunun bulunmaı
            userDailyDb = sql_functions("{}Databases/user{}.db".format(self.dir_path,hex(userIndex)[2:]))#Kullanıcıya özel ,günlük aktivite bilgilerinin saklanacağı veritabanının yaratılması
            userDailyDb.create_table("SleepTable",("Date","TEXT"),("SleepRange","TEXT"),("SleepEfficiency","INT"))#Uyku bilgilerinin saklanacağı tablonun konfigurasyonu

            #Kullanıcıya kayıt bilgisinin başarı durumunun bildirilmesi
            self.registeredNotificationLabel.setText("Kayıt işlemi başarı ile gerçekleştirildi.")
            self.registeredNotificationLabel.setStyleSheet("""
            font-family:Courier;
            font-size:10px;
            font-weight:650;
            color :#5A2C63;
            background-color:#C4FFC1;
            border-left:4px solid  	#35632c;
            padding : 4px;
            """)
            self.registeredNotificationImage.setPixmap(QPixmap("{}Images/tickIconAdjusted.png".format(self.dir_path)))
            QTimer.singleShot(3000,lambda:self.registeredNotificationLabel.setText(""))
            QTimer.singleShot(3000,lambda:self.registeredNotificationLabel.setStyleSheet(""))
            QTimer.singleShot(3000,lambda:self.registeredNotificationImage.setPixmap(QPixmap()))
            QTimer.singleShot(3000,lambda:self.backLogin())#Giriş ekranına geri gelinir


    def backLogin(self):#Giriş ekranına geri yönledirecek fonksiyondur
        from userLogin import userLoginForm#Eğer bu modül başta belirtilir ise import hatası verecektir.
        #Çünkü şu an açılan modülde import edilen modül ile açılmıştır gelmektedir. Eğer başta belirtilmiş olsaydı
        #userLogin modülünden çağırılan bu modül kendisini tekrardan import edecek ve hatalar ortaya çıkacaktır.Bu sebepten ötürü
        #Bu modül burada import edilmiştir.Aynı şey userLogin içindede geçerli olmuştur.Ve bu şekil bir çözüm uygulanmıştır.

        self.close()
        self.openWindow = userLoginForm()
        self.openWindow.show()
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    obj = registrationForm()
    obj.show()
    sys.exit(app.exec_())
