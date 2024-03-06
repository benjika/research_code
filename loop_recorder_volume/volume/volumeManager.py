from joblib import load
import numpy as np
import open3d as o3d
from datetime import datetime


def create_grid(pcloud_np, resolution):
    xy = pcloud_np.T[:2]
    xy = ((xy + resolution / 2) // resolution).astype(int)
    mn, mx = xy.min(axis=1), xy.max(axis=1)
    sz = mx + 1 - mn
    flatidx = np.ravel_multi_index(xy - mn[:, None], sz)
    histo = np.bincount(flatidx, pcloud_np[:, 2], sz.astype(np.int64).prod()) / np.maximum(1, np.bincount(flatidx, None,
                                                                                                          sz.astype(
                                                                                                              np.int64)
                                                                                                          .prod()))
    return histo.reshape(sz), *(xy * resolution)


class VolumeManager:
    def __init__(self):
        self.polynomial_trasnformer1 = load('volume/poly_trasformer1.joblib')
        self.polynomial_trasnformer2 = load('volume/poly_trasformer2.joblib')

        self.regression1 = load('volume/regression1.joblib')
        self.regression2 = load('volume/regression2.joblib')

        self.roi1 = o3d.visualization.read_selection_polygon_volume('volume/crop_coordinates_weight1_Zed.json')
        self.roi2 = o3d.visualization.read_selection_polygon_volume('volume/crop_coordinates_weight2_Zed.json')

    def measure_volume(self, pcd, position_id):

        if np.asanyarray(pcd.points)[:, 2].min() > -100:
            pcd.points = o3d.utility.Vector3dVector(np.asanyarray(pcd.points) * 100)
        if position_id == 1:
            pcd_roi = self.roi1.crop_point_cloud(pcd)
        else:
            pcd_roi = self.roi2.crop_point_cloud(pcd)
        after_points = np.asanyarray(pcd_roi.points)
        after_points = after_points[(-400 <= after_points[:, 2]) & (after_points[:, 2] < -300)]

        try:
            if after_points[:, 2].min() > -10:
                after_points = after_points * 100
            after_grid, x, y = create_grid(after_points, 1)
            volume_cm_cubic = np.sum(after_grid)
            return volume_cm_cubic
        except Exception as e:
            print(e)
            return None

    def process_ply_file(self, hour_path, full_dt_str, position_id, dt):

        file_path = f'{hour_path}/{full_dt_str}_pc.ply'

        pcd = o3d.io.read_point_cloud(file_path)
        total_volume = self.measure_volume(pcd, position_id)
        base_volume, feed_volume = self.remove_base_volume(total_volume, position_id, dt)
        print(f'Measured feed volume position {position_id}: {feed_volume} liters')
        return total_volume, base_volume, feed_volume

    def remove_base_volume(self, total_volume, position_id, dt):

        seconds_since_midnight = (dt - dt.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
        x = np.array(seconds_since_midnight).reshape(1, 1)
        if position_id == 1:
            x_poly = self.polynomial_trasnformer1.transform(x.reshape(-1, 1))
            base_volume = self.regression1.predict(x_poly)[0][0]
        else:
            x_poly = self.polynomial_trasnformer2.transform(x.reshape(-1, 1))
            base_volume = self.regression2.predict(x_poly)[0][0]
        feed_volume_in_cm = total_volume - base_volume
        feed_volume_in_liters = feed_volume_in_cm /1000
        return base_volume, feed_volume_in_liters
