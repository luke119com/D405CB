import pyrealsense2 as rs
import numpy as np
import cv2

# 建立 RealSense pipeline
pipeline = rs.pipeline()
config = rs.config()

# 啟用深度彩流（解析度可自行調整）
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

# 開始串流
pipeline.start(config)

try:
    while True:
        # 等待影像 frame
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        if not depth_frame:
            continue

        # 轉成 numpy array
        depth_image = np.asanyarray(depth_frame.get_data())

        # 用 colormap 讓影像更容易看
        depth_colormap = cv2.applyColorMap(
            cv2.convertScaleAbs(depth_image, alpha=0.08),
            cv2.COLORMAP_JET
        )

        # 取得中心點距離
        h, w = depth_image.shape
        center_distance = depth_frame.get_distance(w//2, h//2)

        # 顯示距離
        text = f"Center Distance: {center_distance:.3f} m"
        cv2.putText(depth_colormap, text, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow("D405 Depth", depth_colormap)

        # 按 ESC 離開
        if cv2.waitKey(1) == 27:
            break

finally:
    pipeline.stop()
    cv2.destroyAllWindows()
