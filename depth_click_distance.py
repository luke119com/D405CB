# -----------------------------------------------------
# 套件檢查區
# -----------------------------------------------------
missing_packages = []

try:
    import pyrealsense2 as rs
except ImportError:
    missing_packages.append("pyrealsense2")

try:
    import cv2
except ImportError:
    missing_packages.append("opencv-python")

try:
    import numpy as np
except ImportError:
    missing_packages.append("numpy")

if missing_packages:
    print("❌ 缺少必要套件：")
    for pkg in missing_packages:
        print(f"   - {pkg}")
    print("\n請使用以下指令安裝：")
    print("pip install " + " ".join(missing_packages))
    exit(1)

# -----------------------------------------------------
# 正式開始
# -----------------------------------------------------
import pyrealsense2 as rs
import numpy as np
import cv2

clicked_point = None  # 儲存滑鼠點擊位置


def mouse_callback(event, x, y, flags, param):
    global clicked_point
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked_point = (x, y)   # 記錄點擊座標


# 建立 RealSense pipeline
pipeline = rs.pipeline()
config = rs.config()

# 啟用深度流
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

# 開始串流
pipeline.start(config)

cv2.namedWindow("D405 Depth Click")
cv2.setMouseCallback("D405 Depth Click", mouse_callback)

print("🎉 已啟動！滑鼠左鍵點擊任意位置可顯示距離。按 ESC 離開。")

try:
    while True:
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        if not depth_frame:
            continue

        depth_image = np.asanyarray(depth_frame.get_data())

        # 美化深度影像
        depth_colormap = cv2.applyColorMap(
            cv2.convertScaleAbs(depth_image, alpha=0.08),
            cv2.COLORMAP_JET
        )

        # 如果使用者有點擊
        if clicked_point:
            x, y = clicked_point
            distance = depth_frame.get_distance(x, y)

            # 畫標記
            cv2.circle(depth_colormap, (x, y), 5, (255, 255, 255), -1)
            cv2.putText(depth_colormap,
                        f"{distance:.3f} m",
                        (x + 10, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                        (255, 255, 255), 2)

        cv2.imshow("D405 Depth Click", depth_colormap)

        if cv2.waitKey(1) == 27:
            break

finally:
    pipeline.stop()
    cv2.destroyAllWindows()
    print("🛑 已停止 RealSense 串流")
