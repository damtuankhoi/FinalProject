import cv2
import os
import numpy as np

image = cv2.imread('D:/Project/frame/frame223.jpg')

# Select ROI 
r = cv2.selectROI("select the area", image) 

# Crop image 
cropped_image = image[int(r[1]):int(r[1]+r[3]),  
                      int(r[0]):int(r[0]+r[2])] 
  
# Display cropped image 
cv2.imshow("Cropped image", cropped_image) 
print("shape of cropped image: ", cropped_image.shape) 
cv2.waitKey(0) 