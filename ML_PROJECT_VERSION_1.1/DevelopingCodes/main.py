#Arayüz çalıştırıcısı modülü
from PyQt5.QtWidgets import QApplication
#Arayüz modülü
from userLogin import userLoginForm
#Sistem modülü
import sys

if __name__ == "__main__":
    # Bu kod parçası yazılımın çalıştırıcı kod parçasıdır.
    # Bu Python dosyası çalıştırılıra yazılım sorunsuzca çalışacaktır.

    # Not Bütün kodlar aynı dizinde ve Images/ dizinide bu dizin altında olmalıdır.
    # Aksi takdirde hata verebilir.
    if sys.platform == "linux":#Bunu CrossPlatformSupport yap.
        app = QApplication(sys.argv)
        obj = userLoginForm()
        obj.show()
        sys.exit(app.exec_())
    else:
        sys.stderr.write("[Hata] Desteklenmeyen platform")
