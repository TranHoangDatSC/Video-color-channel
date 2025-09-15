import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
video_path = BASE_DIR / "input.mkv"
icon_path = BASE_DIR / "icon.png"

cap = cv2.VideoCapture(str(video_path))
fps = cap.get(cv2.CAP_PROP_FPS)
if fps <= 0:
    fps = 30.0

icon = cv2.imread(str(icon_path))
icon_h, icon_w = icon.shape[:2]
pos_x, pos_y = 20, 20

W, H = 640, 360

fig, axs = plt.subplots(2, 2, figsize=(10, 6))
ax1, ax2, ax3, ax4 = axs.ravel()
for ax, title in zip((ax1, ax2, ax3, ax4),
                     ("Original + Icon", "Red Channel", "Green Channel", "Blue Channel")):
    ax.set_title(title); ax.axis("off")

im1 = ax1.imshow(np.zeros((H, W, 3), dtype=np.uint8))
im2 = ax2.imshow(np.zeros((H, W, 3), dtype=np.uint8))
im3 = ax3.imshow(np.zeros((H, W, 3), dtype=np.uint8))
im4 = ax4.imshow(np.zeros((H, W, 3), dtype=np.uint8))
plt.tight_layout()

frame_count = 0
skip = 2   # chỉ vẽ mỗi 2 frame để giảm lag

while True:
    # --- check figure còn tồn tại không ---
    if not plt.fignum_exists(fig.number):
        break

    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (W, H))
    frame[pos_y: pos_y+icon_h, pos_x:pos_x+icon_w] = icon

    b, g, r = cv2.split(frame)
    frame_rgb = frame[..., ::-1]

    if frame_count % skip == 0:
        red   = np.zeros_like(frame_rgb); red[:,:,0] = r
        green = np.zeros_like(frame_rgb); green[:,:,1] = g
        blue  = np.zeros_like(frame_rgb); blue[:,:,2] = b

        im1.set_data(frame_rgb)
        im2.set_data(red)
        im3.set_data(green)
        im4.set_data(blue)

        fig.canvas.draw_idle()
        plt.pause(0.001)  # nhỏ nhất để UI responsive

    frame_count += 1

cap.release()
plt.close(fig)
