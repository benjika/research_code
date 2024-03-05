import pyzed.sl as sl
import numpy as np
import open3d as o3d
import cv2


class CameraManager:
    def __init__(self):
        self.zed = sl.Camera()
        print('Initializing Zed camera')
        # Configure camera in neural mode and set to static position
        init_params = sl.InitParameters()
        #init_params.camera_resolution = sl.RESOLUTION.HD720
        init_params.camera_fps = 15
        init_params.coordinate_units = sl.UNIT.CENTIMETER
        init_params.depth_mode = sl.DEPTH_MODE.ULTRA
        init_params.sdk_verbose = False
        init_params.depth_minimum_distance = 200  # in mm, i.e. 2 meters
        init_params.depth_maximum_distance = 5000  # in mm, i.e. 5 meters
        init_params.coordinate_system = sl.COORDINATE_SYSTEM.RIGHT_HANDED_Y_UP
        #init_params.depth_stabilization = True
        #init_params.sensors_required = False
        #init_params.enable_right_side_measure = False
        #init_params.depth_stabilization = True
        #init_params.camera_disable_self_calib = True
        #init_params.camera_image_flip = False
        #init_params.camera_disable_stream_infos = True
        positional_tracking_parameters = sl.PositionalTrackingParameters()
        positional_tracking_parameters.set_as_static = True
        self.zed.enable_positional_tracking(positional_tracking_parameters)

        err = self.zed.open(init_params)
        if err != sl.ERROR_CODE.SUCCESS:
            print(f"ZED Camera error: {err}")
            exit(1)
        print('Initializing Zed camera complete!')

    def capture_image(self, hour_path, full_dt_str):
        print('Capturing Zed image')
        runtime_params = sl.RuntimeParameters()
        left_image = sl.Mat()
        err = self.zed.grab(runtime_params)
        if err == sl.ERROR_CODE.SUCCESS:
            self.zed.retrieve_image(left_image, sl.VIEW.LEFT)
            left_image_np = np.array(left_image.get_data())
            success =cv2.imwrite(f'{hour_path}/{full_dt_str}_rgb.png', left_image_np)
            print('Capturing d455 image complete! {result}'.format(
            result='Success' if success else 'Error'))
            return success
        else:
            print(f"ZED Camera grab error: {err}")
            return False

    def capture_pointcloud(self, hour_path, full_dt_str):
        print('Capturing Zed pointcloud')
        runtime_params = sl.RuntimeParameters()

        point_cloud = sl.Mat()
        image = sl.Mat()

        err = self.zed.grab(runtime_params)
        if err == sl.ERROR_CODE.SUCCESS:
            self.zed.retrieve_measure(point_cloud, sl.MEASURE.XYZRGBA)
            self.zed.retrieve_image(image, sl.VIEW.LEFT)
            point_cloud_np = point_cloud.get_data()[:, :, :3]
            colors_np = image.get_data()[:, :, :3]

            # Reshape point cloud and colors
            point_cloud_flat = point_cloud_np.reshape(-1, 3)
            colors_flat = colors_np.reshape(-1, 3)

            # Filter out invalid or NaN values
            valid_mask = np.isfinite(point_cloud_flat).all(axis=1)
            point_cloud_filtered = point_cloud_flat[valid_mask]
            colors_filtered = colors_flat[valid_mask]

            # Convert point cloud coordinates to single precision (float)
            point_cloud_float = point_cloud_flat.astype(np.float32)

             # Clip colors to the valid range [0, 255]
            colors_clipped = np.clip(colors_filtered, 0, 255)

            # Convert colors to unsigned 8-bit integers (uint8)
            colors_uint8 = colors_clipped.astype(np.uint8)

            # Create Open3D point cloud and set points and colors
            pcd = o3d.geometry.PointCloud()
            pcd.points = o3d.utility.Vector3dVector(point_cloud_float)
            pcd.colors = o3d.utility.Vector3dVector(colors_flat / 255.0)  # Normalize colors to [0, 1]
            pcd = pcd.remove_non_finite_points()


            # Save point cloud
            success = o3d.io.write_point_cloud(f'{hour_path}/{full_dt_str}_pc.ply', pcd, write_ascii=True)
            print('Capturing Zed pointcloud! {result}'.format(
            result='Success' if success else 'Error'))

            return success
        else:
            print(f"ZED Camera grab error: {err}")
            return False

    def close_camera(self):
        print('Closing Zed camera')
        self.zed.close()
        print('Closing Zed complete')