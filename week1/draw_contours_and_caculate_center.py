import cv2
import os
import numpy as np
from icecream import ic
import matplotlib.pyplot as plt

# lấy danh sách tất cả các tệp trong thư mục
files = os.listdir('D:/Project/frame/')

# định nghĩa ROI (x, y, width, height)
roi = (0, 160, 320, 24)

for file in files:
    # đọc ảnh
    image = cv2.imread('D:/Project/frame/' + file)
    
    # crop bầu trời, chỉ lấy đường chân trời của 2 lane
    img_cropped = image[50:240, 0:320]
    height_origin, weight_origin, __ = img_cropped.shape
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
    N = np.array([95, 0])  # khoảng cách từ điểm tâm của bounding box đến điểm tâm của đường nối

    height, width, _ = img_cropped.shape # height, width, _ = (24, 320, 3)

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

    # Nếu có 2 bounding box, tính toán tọa độ tâm của đường nối
    if len(centers) == 2:
        cv2.line(thresholded, centers[0], centers[1], (255, 0, 0), 2)
        center_x = int((centers[0][0] + centers[1][0]) / 2)
        center_y = int((centers[0][1] + centers[1][1]) / 2)

        # Calculate translation vector
        translation_vector_x = center_x - roi[0]
        translation_vector_y = center_y - roi[0]
        translation_vector = (translation_vector_x, translation_vector_y)

        cv2.circle(thresholded, (center_x, center_y), radius=1, color=(0, 255, 0), thickness=2)

    # Nếu chỉ có 1 bounding box, tâm của đường nối là tâm của bounding box
    elif len(centers) == 1:
        center_x, center_y = centers[0]

# -----------------------đoạn code sau tìm xem đường cong trái hay phải-----------------------
        rows, cols = img.shape[:2]
        [vx, vy, x, y] = cv2.fitLine(contour, cv2.DIST_L2, 0, 0.01, 0.01)
        
        ic('center_y: ',center_y)

        # Xác định xem đường này biểu thị đường cong trái hay phải
        if vx < 0:
            curve_type = "đường cong phải"
            translation_vector_x = width
            translation_vector_y = center_y
        else:
            curve_type = "đường cong trái"
            translation_vector_x = center_x - center_x
            translation_vector_y = center_y

        translation_vector = (translation_vector_x, translation_vector_y)

        print("Curve Type:", curve_type)
# ---------------------------------------------------------------------------
        
    cv2.imshow('Image with bounding boxes', img)
    ic("The translation vector is:", translation_vector)
    cv2.waitKey(0)

    # # vẽ đường nối giữa 2 tâm
    # img = cv2.line(img, centers[0], centers[1], (255, 0, 0), 2)

    # # tính toán tọa độ tâm của đường nối
    # line_center_x = int((centers[0][0] + centers[1][0]) / 2)
    # line_center_y = int((centers[0][1] + centers[1][1]) / 2)

    # # vẽ tâm của đường nối
    # img = cv2.circle(img, (line_center_x, line_center_y), radius=1, color=(0, 255, 0), thickness=2)

    # # tính toán vector khoảng cách giữa 2 tâm
    # distance_vector = (centers[0][0] - line_center_x, centers[0][1] - line_center_y)

    # # in ra khoảng cách
    # print("The distance from the center point of the first bounding box to the center point of the line is:", distance_vector)
    # cv2.imshow('Image with bounding boxes', img)
    # cv2.waitKey(0)
