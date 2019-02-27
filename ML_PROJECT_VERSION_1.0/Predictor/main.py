#Arayüz çalıştırıcısı modülü
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
#Arayüz modülü
from userLogin import userLoginForm
from dirPath import get_dir_path
#Sistem modülü
import sys

if __name__ == "__main__":
    # Bu kod parçası yazılımın çalıştırıcı kod parçasıdır.
    # Bu Python dosyası çalıştırılıra yazılım sorunsuzca çalışacaktır.

    # Not Bütün kodlar aynı dizinde ve Images/ dizinide bu dizin altında olmalıdır.
    # Aksi takdirde hata verebilir.
    app = QApplication(sys.argv)
    obj = userLoginForm()
    obj.setWindowIcon(QIcon(get_dir_path()+"Images/prediction.png"))
    obj.show()
    sys.exit(app.exec_())