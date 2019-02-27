from sqliteModule import sql_functions
from dirPath import get_dir_path
def usersConf():
    # Bu fonksiyon bir nevi setup fonksiyonudur.UserLogin ilk çalıştığında çalışır 
    # ve kullanıcıların kayıt bilgilerinin saklanacağı veritabanının konfigürasyonu yapılır.
    mainDirPath = get_dir_path()
    userDb = sql_functions("{}Databases/users.db".format(mainDirPath))
    userDb.create_table("Users",("Date","TEXT"),("Email","TEXT"),("Username","TEXT"),("Name","TEXT"),("Surname","TEXT"),("Password","TEXT"))


def tableCheck(database_path,table_name):
    sqlObj = sql_functions(database_path)
    if sqlObj.getTableInfo(table_name) == []:
        return False
    else:
        return True

def checkTablesExisitance(database_path,tables_list):
    if isinstance(tables_list,list):
        tableStatusList = [tableCheck(database_path,table) for table in tables_list]
        return tableStatusList
    elif isinstance(tables_list,str):
        return tableCheck(database_path,tables_list)

if __name__ == "__main__":
    print(checkTablesExisitance("/home/wasptheslimy/Desktop/ML_Project_Version1.0/Databases/user0.db",["25-02-2019","21-02-2019","22-02-2019"]))