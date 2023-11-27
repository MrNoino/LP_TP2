import random
import threading
import datetime
import csv
import os
import time

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
        self.updateConfig()
        
    def getIntVaria(self):
        return self.__intVaria
    
    def setIntVaria(self, newIntVaria):
        self.__intVaria = newIntVaria
        self.updateConfig()
        
    def updateConfig(self, filename='config.csv'):
        # Atualizar o ficheiro de config
        with open(filename, 'w') as f:
            writer = csv.DictWriter(f, lineterminator="\n", fieldnames=["IDEAL_HUMIDITY", "IDEAL_HIMIDITY_RANGE"])
            writer.writeheader()
            writer.writerow({"IDEAL_HUMIDITY": self.__vIdeal, "IDEAL_HIMIDITY_RANGE": self.__intVaria})
        
    def read_config(self, filename='config.csv'):
        file_exists = os.path.isfile(filename)
        if file_exists:
            with open(filename, 'r') as file:
                lines = file.readlines()
                if(lines != None):
                    data = lines[1].split(',')
                    self.__vIdeal, self.__intVaria = float(data[0]),float(data[1])
    
    def decideIrrigation(self, obj):
        if(obj["humidity"] < self.__vIdeal):
            if(obj["humidity"] < self.__vIdeal - self.__intVaria):
                if(obj["probRain"] < self.__probRain):
                    return True
        
        return False

    def read_data(self):
        while True:
            
            api = AccuWeather()
            obj = {}
                        
            obj['humidity'] = float(random.random())*100
            # obj['probRain'] = float(random.random())*100
            obj['probRain'] = read_probRain()
            
            obj['irrigation'] = self.decideIrrigation(obj)
            
            obj['vIdeal'] = self.__vIdeal
            obj['intVaria'] = self.__intVaria
            
            # obj['timestamp'] = datetime.datetime.now()
            self.store_data(obj)
            if self.clb is not None:
                self.clb(obj)
            time.sleep(10)
            
    def read_probRain(self):
        return api.getRainProbability(part_of_day="Day")
        # if(obj['probRain'] is None):
        #     self.read_probRain()
        # else:
        #     # escrever o valor colhido no ficheiro
    
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
        