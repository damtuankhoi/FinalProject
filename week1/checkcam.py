import cv2

capture = cv2.VideoCapture('/home/khoi/PycharmProjects/FinalProject/threading/videotest.mp4')
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# VideoWriter = cv2.VideoWriter('C:/Users/KhoiDam/PycharmProjects/video.avi', fourcc, 30.0, (320, 240))

while True:
    ret, frame = capture.read()
    cv2.imshow('frame', frame)
    # VideoWriter.write(frame)
    if cv2.waitKey(0) & 0xFF == ord('q'):
        break

capture.release()
# VideoWriter.release()
cv2.destroyAllWindows()