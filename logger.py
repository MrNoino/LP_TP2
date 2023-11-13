#import adafruit_tsl2591
#import adafruit_sht31d
#import board
#import serial
import random
import threading
import datetime
import csv
import os
import time

class Logger(object):
    vlIdeal = 80
    intVaria = 20
    probRainIdeal = 75
    
    def __init__(self, port='/dev/ttyACM0', filename='data.csv'):
        '''self.ser = serial.Serial(port)
        self.i2c = board.I2C()
        self.tsl = adafruit_tsl2591.TSL2591(self.i2c)
        self.sht = adafruit_sht31d.SHT31D(self.i2c)'''
        self.filename = filename
        self.clb = None
        self.thr = threading.Thread(target=self.read_data)
        self.thr.daemon = True
        self.thr.start()
        
    
    def decideIrrigation(self, obj):
        
        if(obj["humidity"] < self.vlIdeal):
            if(obj["humidity"] < self.vlIdeal - self.intVaria):
                if(obj["probRain"] < self.probRainIdeal):
                    return True
        
        return False

    def read_data(self):
        while True:
            # data = self.ser.readline().decode()
            obj = {}
            '''if data[0] == '$' and data[-3] == '#':
                params = data.split(',')
                for p in params:
                    if '=' in p:
                        attr = p.split('=')
                        obj[attr[0]] = float(attr[1])
                obj['luminosity'] = float(self.tsl.lux)
                obj['temperature'] = float(self.sht.temperature)
                obj['humidity'] = float(self.sht.relative_humidity)
                #obj['timestamp'] = datetime.datetime.now()
                self.store_data(obj)
                if self.clb is not None:
                    self.clb(obj)'''
            
            obj['humidity'] = float(random.random())*100
            obj['probRain'] = float(random.random())*100
            
            obj['irrigation'] = self.decideIrrigation(obj)
            
            
            
            # obj['timestamp'] = datetime.datetime.now()
            # self.store_data(obj)
            if self.clb is not None:
                self.clb(obj)
            time.sleep(15)
    
    def store_data(self, data):
        file_exists = os.path.isfile(self.filename)
        with open(self.filename, 'a') as f:
            writer = csv.DictWriter(f, fieldnames=data.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(data)

    def on_data_updated(self, clb):
        self.clb = clb
        