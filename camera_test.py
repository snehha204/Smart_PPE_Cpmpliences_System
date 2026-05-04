
"""This script tests if the camera is working properly by displaying the video feed 
from the default camera."""
import cv2
# Open the default camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        print("Camera not detected")
        break

    cv2.imshow("Camera Test", frame)

    # Press ESC key to exit
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()