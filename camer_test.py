import cv2

cam = cv2.VideoCapture(0)

if cam.isOpened():
    print("Camera detected!")
else:
    print("No camera found")

cam.release()
