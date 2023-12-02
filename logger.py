import random
import threading
import datetime
import csv
import os
import time
import configparser

from AccuWeather_API import AccuWeather

class Logger(object):
    
    def __init__(self, filename='data.csv'):
        self.__probRainIdeal = 75
        self.__vIdeal = None
        self.__intVaria = None
        self.read_config()
        self.filename = filename
        self.clb = None
        self.thr = threading.Thread(target=self.read_data)
        self.thr.daemon = True
        self.thr.start()
        # self.thr.join()


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


    def write_propertie(self, key, value, filename='config.properties'):
        config = configparser.ConfigParser()
        config.read(filename)
        
        # Adiciona ou atualiza o novo valor
        config['DEFAULT'][key] = str(value)

        # Escreve todas as informações de volta ao arquivo
        with open(filename, 'w') as configfile:
            config.write(configfile)
            
    def read_propertie(self, key, filename='config.properties'):
        
        config = configparser.ConfigParser()
        config.read(filename)
        
        return config['DEFAULT'][key]


    def update_config(self):
        self.write_propertie("humidity_ideal", self.__vIdeal)
        self.write_propertie("humidity_ideal_range", self.__intVaria)
        
    def read_config(self):
        self.__vIdeal = float(self.read_propertie("humidity_ideal"))
        self.__intVaria = float(self.read_propertie("humidity_ideal_range"))


    def decideIrrigation(self, obj):
        if(obj["humidity"] < self.__vIdeal):
            if(obj["humidity"] < self.__vIdeal - self.__intVaria):
                if(obj["probRain"] < self.__probRainIdeal):
                    return True
        
        return False


    def read_data(self):
        while True:
            
            obj = {}
                        
            obj['humidity'] = round(random.random() * 100, 5)
            obj['probRain'], obj['timestamp'] = self.probRain()
            
            obj['irrigation'] = self.decideIrrigation(obj)
            
            obj['vIdeal'] = self.__vIdeal
            obj['intVaria'] = self.__intVaria
            
            self.store_data(obj)
            if self.clb is not None:
                self.clb(obj)
            time.sleep(600)
            
    def probRain(self):
        
        api = AccuWeather()        
        
        now = datetime.datetime.now()
        after_12_hour = datetime.datetime.strptime(self.read_propertie("datetime_rain_probability"),
                                                   "%Y-%m-%d %H:%M:%S.%f") + datetime.timedelta(hours=12)
        # print("Hora atual:",now)
        # print("depois 12h:", after_12_hour)

        if (now > after_12_hour):
            
            partDay = "Day"
            day = 1
            if (now.strftime("%H") < "12"):
                partDay = "Night"
                day = 0
                
            probRain = api.getRainProbability(offset_day=day, part_of_day=partDay)
            print("new value API AccuWeather.")
            
            if(probRain is not None):
                print("API AccuWeather return ok.")
                self.write_propertie("rain_probability", probRain)
                self.write_propertie("datetime_rain_probability", now)
                return probRain, now.strftime("%Y-%m-%d %H:%M:%S")
            
        return float(self.read_propertie("rain_probability")), now.strftime("%Y-%m-%d %H:%M:%S")


    def store_data(self, data):
        file_exists = os.path.isfile(self.filename)
        with open(self.filename, 'a') as f:
            writer = csv.DictWriter(f, lineterminator="\n", fieldnames=data.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(data)


    def read_last_lines(self, n):
        data = {'humidity': [], 'probRain': [], 'irrigation': [],'vIdeal': [], 'intVaria': [],'timestamp': []}
        file_exists = os.path.isfile(self.filename)
        if file_exists:
            with open(self.filename, 'r') as file:
                lines = file.readlines()
                last_n_lines = lines[-n:]
                for line in last_n_lines:
                    values = line.strip().split(',')
                    data['humidity'].append(float(values[0]))
                    data['probRain'].append(float(values[1]))
                    data['timestamp'].append(values[2])
                    data['irrigation'].append(values[3]=='True')
                    data['vIdeal'].append(float(values[4]))
                    data['intVaria'].append(float(values[5]))
        return data


    def on_data_updated(self, clb):
        self.clb = clb
        