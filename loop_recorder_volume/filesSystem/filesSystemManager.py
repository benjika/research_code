import os
from datetime import datetime
import csv
import os.path
import shutil
import subprocess
import pandas as pd


class FilesSystemManager:
    def __init__(self):
        self.path_to_storage = '/data'

    def save_csv(self, data, csv_subject, folder_path, dt):
        # if csvdata.dest == destination_type.day:
        #    folder_path = self.get_day_path(csvdata.dt)
        # elif CsvData.dest == destination_type.hour:
        #    folder_path == self.get_hour_path(csvdata.dt)
        file_path = f'{os.path.join(folder_path, csv_subject)}.csv'
        print(file_path)
        row = [dt.strftime("%H:%M:%S %d/%m/%Y")] + data
        with open(file_path, 'a+') as f:
            writer = csv.writer(f)
            writer.writerow(row)

    def get_day_path(self, dt: datetime):
        day_str = dt.strftime("%d_%m_%Y")
        day_path = os.path.join(self.path_to_storage, day_str)
        if not os.path.isdir(day_path):
            os.mkdir(day_path)
        return day_path

    def get_hour_path(self, dt: datetime):
        hour_str = dt.strftime("%H")
        day_path = get_day_path(dt)
        hour_path = os.path.join(day_path, hour_str)
        if not os.path.isdir(hour_path):
            os.mkdir(hour_path)
        return hour_path

    def get_disk_path(self):
        columns = (
            ' '.join(str(subprocess.check_output(['lsblk', '-l'])).split("\\n")[0].replace("b'", '').split())).split()

        mounts_rows = []

        for line in str(subprocess.check_output(['lsblk', '-l'])).split("\\n")[1:]:
            parts = (' '.join(line.split())).split()
            data = {}
            for i, col in enumerate(columns):
                if i >= len(parts):
                    data[col] = ''
                else:
                    data[col] = parts[i].replace(' ', '')

            mounts_rows.append(data)

        mounts_df = pd.DataFrame(mounts_rows, columns=columns)

        mounts_df = mounts_df[(mounts_df.TYPE == 'part') & (
                mounts_df.MOUNTPOINT.astype('str').str.len() > 1)]

        mounts_df['FREE_DISK'] = mounts_df.MOUNTPOINT.apply(
            lambda x: shutil.disk_usage(x).free)

        min_free_space_threshold = 2 * 1073741824#5 * 1073741824

        mounts_df = mounts_df[mounts_df.FREE_DISK > min_free_space_threshold]

        mounts_df = mounts_df.sort_values('FREE_DISK').reset_index(drop=True)

        if len(mounts_df) == 0:
            print('No connected disks')
            return None
        else:
            return mounts_df.loc[0, 'MOUNTPOINT']
