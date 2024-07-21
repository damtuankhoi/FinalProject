import cv2
import os
import numpy as np
import matplotlib.pyplot as plt

# định nghĩa ROI (x, y, width, height)
roi = (0, 160, 320, 24)

image = cv2.imread("D:/Project/frame/frame172.jpg")

# crop bầu trời, chỉ lấy đường chân trời của 2 lane
img_cropped = image[50:240, 0:320]

# sau khi crop, chỉ lấy ROI
img_cropped = img_cropped[roi[1]:roi[1] + roi[3], roi[0]:roi[0] + roi[2]]

# chuyển ảnh sang ảnh xám
gray = cv2.cvtColor(img_cropped, cv2.COLOR_BGR2GRAY)

# Áp dụng ngưỡng nhị phân cho hình ảnh để chỉ giữ lại các pixel màu trắng
_, thresholded = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

# Tìm contours
contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Sắp xếp các contour theo diện tích theo thứ tự giảm dần và lấy hai contour đầu tiên
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:2]

centers = []

# lặp qua tất cả các contours:
for contour in contours:
    # lấy tọa độ của bounding box
    x, y, w, h = cv2.boundingRect(contour)

    # tính toán tọa độ tâm của bounding box
    center_x = int(x + w / 2)
    center_y = int(y + h / 2)

    # thêm tọa độ tâm vào list
    centers.append((center_x, center_y))

    # vẽ bounding box
    img = cv2.rectangle(thresholded, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # vẽ tâm của bounding box
    img = cv2.circle(img, (center_x, center_y), radius=1, color=(0, 255, 0), thickness=2)

    rows, cols = img.shape[:2]
    [vx, vy, x, y] = cv2.fitLine(contour, cv2.DIST_L2, 0, 0.01, 0.01)
    
    # Xác định xem đường này biểu thị đường cong trái hay phải
    if vx < 0:
        curve_type = "đường cong phải"
    else:
        curve_type = "đường cong trái"

    print("Curve Type:", curve_type)
# -----------------------------------test---------------------------------------
    # Transpose and flip the image vertically
    image = np.flipud(image)

    # Create figure and axis
    fig, ax = plt.subplots()

    # Display the image
    ax.imshow(image, origin='lower')

    # Get image dimensions
    width, height, _ = image.shape

    # Set aspect ratio
    aspect_ratio = width / height

    # Plotting example
    plt.plot([0, 1], [0, 1])  # Just a dummy plot for demonstration

    # Set aspect ratio of the plot
    plt.gca().set_aspect(aspect_ratio)

    # Adjust axis limits to match image aspect ratio
    plt.xlim(0, 320)
    plt.ylim(0, 24)

    # Show plot
    plt.show()
# -----------------------------------------------------------------------------------------------
    
    # lefty = int((-x * vy / vx) + y)
    # righty = int(((cols - x) * vy / vx) + y)
    # img = cv2.line(img, (cols - 1, righty), (0, lefty), (0, 255, 0), 2)

    cv2.imshow('img', img)
    cv2.waitKey(0)
