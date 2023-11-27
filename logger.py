import random
import threading
import datetime
import csv
import os
import time
from jproperties import Properties

from AccuWeather_API import AccuWeather

class Logger(object):
    
    def __init__(self, filename='data.csv'):
        self.__probRainIdeal = 75
        self.__vIdeal = None
        self.__intVaria = None
        self.filename = filename
        self.clb = None
        self.thr = threading.Thread(target=self.read_data)
        self.thr.daemon = True
        self.thr.start()
        self.read_config()


    def getVIdeal(self):
        return self.__vIdeal
    
    def setVIdeal(self, newVIdeal):
        self.__vIdeal = newVIdeal
        self.update_config()
        
    def getIntVaria(self):
        return self.__intVaria
    
    def setIntVaria(self, newIntVaria):
        self.__intVaria = newIntVaria
        self.update_config()


    def write_propertie(self, key, value, filename='LP_TP2/config.properties'):
        # Atualizar o ficheiro de config
        p = Properties()
        with open(filename, "w+b") as f:
            p.load(f, "utf-8")
            
            p[key] = str(value)

            f.seek(0)
            f.truncate(0)
            p.store(f, encoding="utf-8")
            
    def read_propertie(self, key, filename='LP_TP2/config.properties'):
        
        p = Properties()
                    
        with open(filename, "rb") as f:
            p.load(f, "utf-8")
            # print(p.get(key)[0])
            output = p.get(key)[0]
        
        return output
    
    
    def update_config(self):
        self.write_propertie("huminity_ideal", self.__vIdeal)
        self.write_propertie("huminity_ideal_range", self.__intVaria)
        
    def read_config(self):
        self.__vIdeal = float(self.read_propertie("huminity_ideal"))
        self.__intVaria = float(self.read_propertie("huminity_ideal_range"))


    def decideIrrigation(self, obj):
        if(obj["humidity"] < self.__vIdeal):
            if(obj["humidity"] < self.__vIdeal - self.__intVaria):
                if(obj["probRain"] < self.__probRainIdeal):
                    return True
        
        return False


    def read_data(self):
        while True:
            
            obj = {}
                        
            obj['humidity'] = float(random.random())*100
            obj['probRain'] = self.probRain()
            
            obj['irrigation'] = self.decideIrrigation(obj)
            
            obj['vIdeal'] = self.__vIdeal
            obj['intVaria'] = self.__intVaria
            
            # obj['timestamp'] = datetime.datetime.now()
            self.store_data(obj)
            if self.clb is not None:
                self.clb(obj)
            time.sleep(10)
            
    def probRain(self):
        
        api = AccuWeather()        
        
        # Obtém o tempo atual
        now = datetime.datetime.now()
        # Adiciona 12 horas a tempo da última coleta
        after_12_hour = datetime.datetime.strptime(self.read_propertie("datetime_rain_probability"),
                                                   "%Y-%m-%d %H:%M:%S") + datetime.timedelta(hours=12)
        # print("Hora atual:", agora)
        # print("Hora depois de 12 horas:", depois_de_12_horas)

        if (now > after_12_hour):
            probRain = api.getRainProbability(part_of_day="Day")
            if(probRain is not None):
                self.write_propertie("rain_probability", probRain)
                return probRain
            
        return float(self.read_propertie("rain_probability"))


    def store_data(self, data):
        file_exists = os.path.isfile(self.filename)
        with open(self.filename, 'a') as f:
            writer = csv.DictWriter(f, lineterminator="\n", fieldnames=data.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(data)

       
    def read_last_lines(self, n):
        file_exists = os.path.isfile(self.filename)
        if file_exists:
            with open(self.filename, 'r') as file:
                lines = file.readlines()
                last_n_lines = lines[-n:]
                return last_n_lines


    def on_data_updated(self, clb):
        self.clb = clb
        