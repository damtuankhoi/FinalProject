import pyrealsense2 as rs
import numpy as np
import cv2

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

color_path = 'FinalProject/rs_camera/ColorImg/V00P00A00C00_rgb.avi'
depth_path = 'FinalProject/rs_camera/DepthImg/V00P00A00C00_depth.avi'
colorwriter = cv2.VideoWriter(color_path, cv2.VideoWriter_fourcc(*'XVID'), 30, (640,480), 1)
depthwriter = cv2.VideoWriter(depth_path, cv2.VideoWriter_fourcc(*'XVID'), 30, (640,480), 1)

pipeline.start(config)

try:
    while True:
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        if not depth_frame or not color_frame:
            continue
        
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
        
        width = depth_frame.get_width()
        height = depth_frame.get_height()
        center_distance = depth_frame.get_distance(width // 2, height // 2)
        
        distance_text = f"Distance: {center_distance:.2f} meters"
        cv2.putText(depth_colormap, distance_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        colorwriter.write(color_image)
        depthwriter.write(depth_colormap)
        
        cv2.imshow('Stream', depth_colormap)
        
        if cv2.waitKey(1) == ord("q"):
            break
finally:
    colorwriter.release()
    depthwriter.release()
    pipeline.stop()