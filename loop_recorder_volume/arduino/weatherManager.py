import numpy as np
import serial


class WeatherManager:
    def __init__(self, port: str):
        self.port = port
        self.serial = None
        self.connect_to_serial()

    def connect_to_serial(self):
        if self.port is None:
            print(f'Weather has no port')
            return
        self.serial = serial.Serial(self.port, 9600, timeout=3)

    def measure(self):
        try:
            print(f'weather started')
            temperature_arr, altitude_arr, pressure_arr, hum_arr = [], [], [], []
            for _ in range(3):
                line_data = (self.serial.readline()[:-2]).decode().split()

            for _ in range(10):
                line_data = (self.serial.readline()[:-2]).decode().split(',')
                print(line_data)
                if 'started' in line_data[0]:
                    continue
                if len(line_data) != 4:
                    continue
                read_temperature = float(line_data[0])
                read_pressure = float(line_data[1])
                read_hum = float(line_data[2])
                read_altitude = float(line_data[3])
                temperature_arr.append(read_temperature)
                altitude_arr.append(read_altitude)
                pressure_arr.append(read_pressure)
                hum_arr.append(read_hum)
            temperature = np.mean(temperature_arr)
            alt = np.mean(altitude_arr)
            press = np.mean(pressure_arr)
            hum = np.mean(hum_arr)
            print(f'weather ended')
            return temperature, alt, press, hum
        except Exception as e:
            print(e)
            return None, None, None, None
        finally:
            pass

    def close(self):
        if self.serial is not None:
            self.serial.close()