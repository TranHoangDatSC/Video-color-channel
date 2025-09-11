# Video Channel Splitter with Icon Overlay

## Giới thiệu

Script này đọc một video (`input.mkv`), chèn một icon (`icon.png`) lên video, sau đó hiển thị song song:

- Video gốc (có icon)
- Kênh màu đỏ (Red Channel)
- Kênh màu xanh lá (Green Channel)
- Kênh màu xanh dương (Blue Channel)

Ứng dụng:

- Thực hành xử lý ảnh/video bằng OpenCV.
- Minh họa cách tách kênh màu.
- Overlay ảnh nhỏ lên video.

---

## Công nghệ sử dụng

- **OpenCV (cv2)**: đọc/ghi video, resize, tách kênh màu.
- **Matplotlib**: hiển thị frame theo thời gian thực.
- **NumPy**: xử lý ma trận pixel.
- **Pathlib**: quản lý đường dẫn file an toàn, đa nền tảng.

---

## Cách chạy

1. Cài đặt thư viện:
   ```bash
   pip install opencv-python matplotlib numpy
   ```
