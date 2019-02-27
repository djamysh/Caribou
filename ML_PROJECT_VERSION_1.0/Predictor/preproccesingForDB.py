import pandas as pd
from sqliteModule import sql_functions
import os


class preproccesedData():

    def __init__(self,dayTableColumns,sleepTableColumns,rawDatabasePath, *args, **kwargs):
        self.dayTableColumns = dayTableColumns
        self.sleepTableColumns = sleepTableColumns
        
        if os.path.isfile(rawDatabasePath):
            self.rawDatabasePath = rawDatabasePath
            self.__RawDB = sql_functions(self.rawDatabasePath)
        else:
            raise FileNotFoundError("Geçersiz veritabanı konumu.")

        self.__data_dict = dict()

    def __databaseToArray(self):
        for table in self.__RawDB.tableList():
            table = table[0]
            data = self.__RawDB.get_whole_table(table)


            for iteration in data:
                raw = list(iteration)
                
                if table != "SleepTable":
                    job = iteration[0]
                    raw.pop(0)
                    raw.insert(0,table)

                else:
                    job = table 


                try:
                    self.__data_dict[job].append(raw)
                except KeyError:
                    self.__data_dict[job] = list()
                    self.__data_dict[job].append(raw)





    def __arrayToDataFrame(self):#istihza adlı kitapta kodların obje kullanıcısına gizlemeyi öğren..
        for key in self.__data_dict:
            info = self.__data_dict[key]
            
            if key == "SleepTable":
                df = pd.DataFrame(data = info,index = range(len(info)),columns = self.sleepTableColumns)

            else:

                df = pd.DataFrame(data=info,index = range(len(info)),columns = self.dayTableColumns)

            self.__data_dict[key] = df


    @property
    def get_data_Dict(self):
        self.__databaseToArray()
        self.__arrayToDataFrame()
        return self.__data_dict


if __name__ == "__main__":
    dayTableColumns = ["Date","TimeRange","Willingness","Fatigue","OperationDifficulty","Morale","Efficiency"]
    sleepTableColumns = ["Date","SleepRange","SleepEfficiency"]
    path = "/home/wasptheslimy/NewIdiotqueIdea/CleanCodes/UserDatabase.db"
    obj = preproccesedData(dayTableColumns = dayTableColumns,sleepTableColumns=sleepTableColumns,rawDatabasePath =path )
    ADJ_data = obj.get_data_Dict
    for keys in ADJ_data:
        print("ACTIVITY : ",keys,"\n",ADJ_data[keys])
        print("#"*48)
        
    