import random
import threading
import datetime
import csv
import os
import time

from AccuWeather_API import AccuWeather

class Logger(object):
    
    
    
    def __init__(self, filename='data.csv'):
        self.probRainIdeal = None
        self.vIdeal = None
        self.intVaria = None
        self.probRain = None
        self.humidity = None
        self.irrigation = None
    
        self.filename = filename
        last_line = self.read_last_lines(2)
        if(last_line != None):
            dados = last_line[0].split(',')
            self.humidity, self.probRain = float(dados[0]),float(dados[1])
            self.irrigation = bool(dados[2])
            self.vIdeal, self.intVaria = float(dados[3]),float(dados[4])
            # print("Ultimos Dados: ", self.humidity)
            # print("Ultimos Dados: ", self.probRain)
            # print("Ultimos Dados: ", self.irrigation)
            # print("Ultimos Dados: ", self.vIdeal)
            # print("Ultimos Dados: ", self.intVaria)
    
        
        self.clb = None
        self.thr = threading.Thread(target=self.read_data)
        self.thr.daemon = True
        self.thr.start()
        
        
        
    
    def decideIrrigation(self, obj):
        if(obj["humidity"] < self.vIdeal):
            if(obj["humidity"] < self.vIdeal - self.intVaria):
                if(obj["probRain"] < self.probRain):
                    return True
        
        return False

    def read_data(self):
        while True:
            
            api = AccuWeather()
            obj = {}
                        
            obj['humidity'] = float(random.random())*100
            obj['probRain'] = float(random.random())*100
            # obj['probRain'] = api.getRainProbability(part_of_day="Day")
            
            obj['irrigation'] = self.decideIrrigation(obj)
            
            obj['vIdeal'] = self.vIdeal
            obj['intVaria'] = self.intVaria
            
            # obj['timestamp'] = datetime.datetime.now()
            self.store_data(obj)
            if self.clb is not None:
                self.clb(obj)
            time.sleep(10)
            print("A")
    
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
        