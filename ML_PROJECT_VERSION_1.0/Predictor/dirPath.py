#modül yüklemesi
import os 


def get_dir_path():
    # Bu fonksiyon ,bir dosya dizini içinde bulunan kodların bulunduğu dizinin Global 
    # kounumunu verir.Relative(göreceli) konum ile yapılır ise dosyanın konumuna bağlı
    # olarak kodlar çalışmayabilir.Bu kodların nereden çalıştırıldığına bağlıdır.Örneğin
    # /home/ dizini altında çalıştırıldırğında eğer relative konum kullanılıyor ise çalışmaz
    # ama global konum kullanılıyor ise çalıtırılan dizin neresi olursa olsun program çalışacaktır.

    file_path = str(os.path.realpath(__file__))#__file__ çalışan kod dosyasının global konumunu döndürür.
    globalDirPath = ""
    #Burada ise kod dosyasının bulunduğu dizini bulur ve fonksiyonda döndürür.
    for txt in  file_path.split("/")[:-1]:
        globalDirPath += txt + "/"

    return globalDirPath