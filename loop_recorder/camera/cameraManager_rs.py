import pyrealsense2 as rs
import numpy as np
import cv2
import open3d as o3d
import threading
import datetime
import subprocess


resolution_width = 1280  # pixels
resolution_height = 720  # pixels
frame_rate = 15  # fps


class CameraManager:
    def __init__(self):

        # Create a lock for capturing
        self.capture_lock = threading.Lock()

        try:
            # Create a Camera object
            print('Initializing d455 camera')
            # self.restart_camera()
            self.pipeline = rs.pipeline()
            config = rs.config()
            config.enable_stream(
                rs.stream.depth, resolution_width, resolution_height, rs.format.z16, frame_rate)
            config.enable_stream(rs.stream.infrared, 1, resolution_width,
                                 resolution_height, rs.format.y8, frame_rate)
            config.enable_stream(rs.stream.color, resolution_width,
                                 resolution_height, rs.format.bgr8, frame_rate)

            # load very_accurate preset
            self.pipeline.start(config)
            profile = self.pipeline.get_active_profile()

            with open('camera/accurate_preset.json', 'r') as file:
                json_text = file.read().strip()

            device = profile.get_device()
            advanced_mode = rs.rs400_advanced_mode(device)
            advanced_mode.load_json(json_text)

            # Set depth to centimeters
            depth_sensor = profile.get_device().first_depth_sensor()
            depth_sensor.set_option(rs.option.depth_units, 0.01)
            # depth_sensor.set_option(rs.option.min_distance, 200)
            # depth_sensor.set_option(rs.option.max_distance, 500)
            self.colorizer = rs.colorizer()
            print('Initializing d455 camera complete!')
        except Exception as e:
            print(e)

    def capture_image(self, hour_path, full_dt_str):
        print('Capturing d455 image')
        self.capture_lock.acquire()

        try:
            frames = self.pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()
            # depth_frame = frames.get_depth_frame()
            if not color_frame:
                res = False
                self.capture_lock.release()
                return res
            color_image = np.asanyarray(color_frame.get_data())
            res = cv2.imwrite(
                f'{hour_path}/{full_dt_str}_rgb.png', color_image)
            self.capture_lock.release()
            return res
        except Exception as e:
            print(e)
            # self.restart_camera()
            res = False
        self.capture_lock.release()

        print('Capturing d455 image complete! {result}'.format(
            result='Success' if res else 'Error'))

        return res

    def capture_pointcloud(self, hour_path, full_dt_str):
        print('Capturing d455 pointcloud')
        self.capture_lock.acquire()
        try:
            """
            for _ in range(5):
                # Wait for a frame
                frames = self.pipeline.wait_for_frames()

                # Get the depth frame
                depth_frame = frames.get_depth_frame()
                color_frame = frames.get_color_frame()

                if depth_frame and color_frame:
                    break

            if not depth_frame:
                raise Exception('No depth frame was captured')
            if not color_frame:
                raise Exception('No color frame was captured')

            # Create a point cloud from the depth frame
            pc = rs.pointcloud()
            pc.map_to(color_frame)
            points = pc.calculate(depth_frame)

            # Convert the point cloud to Open3D format
            vertices = np.asarray(points.get_vertices())
            colors = np.asarray(color_frame.get_data())

            print(vertices[:5])

            # Filter out invalid points
            valid_indices = np.logical_and(
                vertices[:, 0] != 0,
                np.isfinite(vertices[:, 2])
            )
            vertices = vertices[valid_indices]
            colors = colors[valid_indices]

            # Create an Open3D point cloud object
            pcd = o3d.geometry.PointCloud()
            pcd.points = o3d.utility.Vector3dVector(vertices)
            pcd.colors = o3d.utility.Vector3dVector(colors)

            # Save the point cloud to a PLY file
            res = o3d.io.write_point_cloud("pointcloud.ply", pcd)
            """

            frames = self.pipeline.wait_for_frames()

            colorized = self.colorizer.process(frames)
            ply = rs.save_to_ply(f'{hour_path}/{full_dt_str}_pc.ply')
            ply.set_option(rs.save_to_ply.option_ply_binary, False)
            ply.set_option(rs.save_to_ply.option_ply_normals, False)
            ply.process(colorized)
            res = True

            """
            frames = pipeline.wait_for_frames()

            depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()

            depth_intrinsics = rs.video_stream_profile(
                depth_frame.profile).get_intrinsics()

            depth_image = np.asanyarray(depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())

            pc = rs.pointcloud()
            points = pc.calculate(depth_frame)
            pc.map_to(color_frame)

            ply = rs.save_to_ply(f'{hour_path}/{full_dt_str}_pc.ply')
            ply.set_option(rs.save_to_ply.option_ply_binary, False)
            ply.set_option(rs.save_to_ply.option_ply_normals, False)
            """
        except Exception as e:
            print(e)
            # self.restart_camera()
            res = False
        self.capture_lock.release()

        print('Capturing d455 pointcloud complete! {result}'.format(
            result='Success' if res else 'Error'))

        return res

    def close_camera(self):
        print('Closing d455 camera')
        self.pipeline.stop()
        print('Closing d455 camera complete')

    def restart_camera(self):
        ctx = rs.context()
        devices = ctx.query_devices()
        for dev in devices:
            dev.hardware_reset()
