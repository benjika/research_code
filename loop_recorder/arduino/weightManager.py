import serial
import numpy as np


class WeightManager:
    def __init__(self, weight_num: int, port: str):
        self.weight_num = weight_num
        self.port = port
        self.serial = None
        self.connect_to_serial()

    def connect_to_serial(self):
        if self.port is None:
            print(f'Weight {self.weight_num} has no port')
            return
        self.serial = serial.Serial(self.port, 9600, timeout=3)

    def measure(self):
        try:
            print(f'weight{self.weight_num} started')
            weight_arr = []
            for i in range(10):
                line_data = (self.serial.readline()[:-2]).decode().split()
                if len(line_data) != 2:
                    continue
                if line_data[0] == 'starting':
                    continue
                print(line_data)
                read_weight = float(line_data[1])
                if read_weight < 0:
                    read_weight = 0
                weight_arr.append(read_weight)
            weight = np.mean(weight_arr)
            print(f'weight{self.weight_num} ended')
            return weight
        except Exception as e:
            print(e)

    def close(self):
        if self.serial is not None:
            self.serial.close()