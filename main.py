# --- Thư viện ---
import cv2                # OpenCV: dùng để đọc/ghi video, xử lý ảnh cơ bản (cắt, resize, split channel...)
import matplotlib.pyplot as plt  # Matplotlib: dùng để hiển thị ảnh, vẽ biểu đồ
import numpy as np        # Numpy: xử lý mảng số học (ảnh/video là ma trận pixel)
from pathlib import Path  # Pathlib: quản lý đường dẫn file một cách gọn gàng, đa nền tảng

# --- Chuẩn bị đường dẫn file ---
BASE_DIR = Path(__file__).resolve().parent   # lấy thư mục hiện tại chứa file .py
video_path = BASE_DIR / "input.mkv"          # đường dẫn video input
cap = cv2.VideoCapture(str(video_path))      # mở video để đọc từng frame

icon_path = BASE_DIR / "icon.png"            # đường dẫn icon
icon = cv2.imread(str(icon_path))            # đọc icon (ảnh nhỏ 32x32)
icon_h, icon_w = icon.shape[:2]              # lấy chiều cao (height), chiều rộng (width) của icon

# Vị trí overlay icon lên video (pixel)
pos_x, pos_y = 20, 20

# --- Tạo figure và 4 axes chỉ 1 lần (để không bị "spam n figure") ---
fig, axs = plt.subplots(2, 2, figsize=(10,6))  # 2x2 subplot, khung tổng thể 10x6 inch
ax1, ax2, ax3, ax4 = axs.ravel()               # trải mảng 2x2 thành 4 biến

# Khởi tạo 4 subplot với ảnh đen ban đầu
im1 = ax1.imshow(np.zeros((360,640,3), dtype=np.uint8))
ax1.set_title("Original + Icon"); ax1.axis("off")

im2 = ax2.imshow(np.zeros((360,640,3), dtype=np.uint8))
ax2.set_title("Red Channel"); ax2.axis("off")

im3 = ax3.imshow(np.zeros((360,640,3), dtype=np.uint8))
ax3.set_title("Green Channel"); ax3.axis("off")

im4 = ax4.imshow(np.zeros((360,640,3), dtype=np.uint8))
ax4.set_title("Blue Channel"); ax4.axis("off")

plt.tight_layout()   # căn chỉnh subplot cho gọn gàng

# --- Loop đọc frame ---
while True:
    ret, frame = cap.read()   # ret=True nếu còn frame, False khi hết video
    if not ret:
        break

    # Resize frame về kích thước chuẩn (640x360 pixel) để đồng nhất
    frame = cv2.resize(frame, (640, 360))

    # Overlay icon lên góc trái trên của video
    frame[pos_y: pos_y + icon_h, pos_x : pos_x + icon_w] = icon

    # Tách kênh màu B, G, R (OpenCV mặc định đọc ảnh dạng BGR)
    b, g, r = cv2.split(frame)

    # Chuyển sang RGB để matplotlib hiển thị đúng màu
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Tạo ảnh chỉ giữ 1 kênh màu (Red, Green, Blue)
    red_channel   = np.zeros_like(frame_rgb); red_channel[:,:,0] = r   # kênh đỏ
    green_channel = np.zeros_like(frame_rgb); green_channel[:,:,1] = g # kênh xanh lá
    blue_channel  = np.zeros_like(frame_rgb); blue_channel[:,:,2] = b  # kênh xanh dương

    # Update dữ liệu cho 4 subplot
    im1.set_data(frame_rgb)      # ảnh gốc + icon
    im2.set_data(red_channel)    # chỉ kênh đỏ
    im3.set_data(green_channel)  # chỉ kênh xanh lá
    im4.set_data(blue_channel)   # chỉ kênh xanh dương

    # --- Điều chỉnh tốc độ ---
    # plt.pause(x) sẽ dừng x giây cho mỗi frame
    # 0.0001 giây = 0.1ms gần như bỏ qua delay -> chạy rất nhanh (chế độ "fast preview")
    # Nếu muốn chạy theo tốc độ thật (fps của video), thay bằng:
    #   fps = cap.get(cv2.CAP_PROP_FPS)
    #   delay = 1.0 / fps
    #   plt.pause(delay)
    plt.pause(0.0001)

cap.release()  # đóng video khi đọc xong
plt.close()    # đóng cửa sổ matplotlib
