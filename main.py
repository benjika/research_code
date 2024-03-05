from arduino.arduinoManager import ArduinoManager
from camera.cameraManager_zed import CameraManager
from filesSystem.filesSystemManager import FilesSystemManager
import datetime
import os
import time

arduinoManager = ArduinoManager()
cameraManager = CameraManager()
filesSystemManager = FilesSystemManager()

last_weight1_capture = datetime.datetime.now() - datetime.timedelta(minutes=3)
last_weight2_capture = datetime.datetime.now() - datetime.timedelta(seconds=20)
last_weather_measure = datetime.datetime.now() - datetime.timedelta(minutes=30)
last_image_captured = datetime.datetime.now() - datetime.timedelta(seconds=5)

try:
    while True:
        time.sleep(1)

        disk_path = filesSystemManager.get_disk_path()

        if disk_path is None:
            continue

        is_to_capture_point_cloud = False

        now = datetime.datetime.now()

        data_path = f'{disk_path}/data'
        if not os.path.exists(data_path):
            os.makedirs(data_path)

        day_path = f'{data_path}/{now.strftime("%d_%m_%Y")}'
        if not os.path.exists(day_path):
            os.makedirs(day_path)

        hour_path = f'{day_path}/{now.strftime("%H")}'
        if not os.path.exists(hour_path):
            os.makedirs(hour_path)

        full_dt_str = now.strftime("%H_%M_%S__%d_%m_%Y")

        if now > last_image_captured + datetime.timedelta(seconds=5):
            last_image_captured = now
            img = cameraManager.capture_image(hour_path, full_dt_str)
            if not img:
                cameraManager.restart_camera()

        if now > last_weight1_capture + datetime.timedelta(seconds=20):
            is_to_capture_point_cloud = True
            last_weight1_capture = now
            weight1_data = [arduinoManager.measure_weight1()]
            filesSystemManager.save_csv(
                weight1_data, f'weight1_{now.strftime("%d_%m_%Y")}', day_path, now)

        if now > last_weight2_capture + datetime.timedelta(seconds=20):
            is_to_capture_point_cloud = True
            last_weight2_capture = now
            weight2_data = [arduinoManager.measure_weight2()]
            filesSystemManager.save_csv(
                weight2_data, f'weight2_{now.strftime("%d_%m_%Y")}', day_path, now)

        if now > last_weather_measure + datetime.timedelta(minutes=2):
            last_weather_measure = now
            weather_data = list(arduinoManager.measure_weather())
            filesSystemManager.save_csv(
                weather_data, f'weather_{now.strftime("%d_%m_%Y")}', day_path, now)

        if is_to_capture_point_cloud:
            is_to_capture_point_cloud = False
            cameraManager.capture_pointcloud(hour_path, full_dt_str)

except KeyboardInterrupt:
    cameraManager.close_camera()
    print('interrupted!')
except Exception as e:
    cameraManager.close_camera()
    print(e)
