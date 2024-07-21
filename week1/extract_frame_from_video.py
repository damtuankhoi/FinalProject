import cv2

video = cv2.VideoCapture('LaneDetection/video.mp4')
success, image = video.read()
count = 0

while success:
    cv2.imwrite("Image/frame%d.jpg" % count, image)  # save frame as JPEG file
    success, image = video.read()
    print('Read a new frame: ', success)
    count += 1
