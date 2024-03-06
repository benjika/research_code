import re
import os
import serial
from datetime import datetime
from arduino.weatherManager import WeatherManager
from arduino.weightManager import WeightManager


class ArduinoManager:

    def __init__(self):
        self.weather_manager = None
        self.weight2_manager = None
        self.weight1_manager = None
        self.ports = dict()
        self.init_ports()
        self.init_arduinos()

    def init_ports(self):

        pat = re.compile(r'ttyACM*')
        ports = [
            f'/dev/{port}' for port in list(filter(pat.match, os.listdir('/dev/')))]

        for port in ports:
            arduino = serial.Serial(port, 9600, timeout=3)
            for _ in range(5):
                line = arduino.readline().decode('ISO-8859-1').lower()
                if 'weather' in line or ',' in line and len(line.split(',')) == 4:
                    self.ports['weather'] = port
                    print(f'weather port found: {port}')
                    # arduino.close()
                    break
                elif 'weight1' in line:
                    self.ports['weight1'] = port
                    print(f'weight1 found port: {port}')
                    # arduino.close()
                    break
                elif 'weight2' in line:
                    self.ports['weight2'] = port
                    print(f'weight2 found port: {port}')
                    # arduino.close()
                    break
            # arduino.close()

        if 'weather' not in self.ports.keys():
            print('weather port not found')
        if 'weight1' not in self.ports.keys():
            print('weight1 port not found')
        if 'weight2' not in self.ports.keys():
            print('weight2 port not found')
            return None

    def init_arduinos(self):
        if 'weight1' in self.ports.keys():
            self.weight1_manager = WeightManager(1, self.ports['weight1'])
        if 'weight2' in self.ports.keys():
            self.weight2_manager = WeightManager(2, self.ports['weight2'])
        if 'weather' in self.ports.keys():
            self.weather_manager = WeatherManager(self.ports['weather'])
            return None

    def measure_weight1(self):
        if self.weight1_manager is None:
            print('Weight1 not defined')
            return None
        print(f'started w1 {datetime.now()}')
        w = self.weight1_manager.measure()
        print('ended w1')
        return w

    def measure_weight2(self):
        if self.weight1_manager is None:
            print('Weight2 not defined')
            return None
        print(f'started w2 {datetime.now()}')
        w = self.weight2_manager.measure()
        print('ended w2')
        return w

    def measure_weather(self):
        if self.weather_manager is None:
            print('weather not defined')
            return None, None, None, None
        print('started weather')
        (temperature, alt, press, hum) = self.weather_manager.measure()
        print('ended weather')
        return temperature, alt, press, hum

    def close_arduinos(self):
        pass
