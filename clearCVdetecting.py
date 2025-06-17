import cv2
import numpy as np

img = cv2.imread("greenTest/perfects/IMG_1244.jpeg")
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Диапазон белого цвета
lower_white = np.array([0, 0, 200])
upper_white = np.array([180, 20, 255])

mask = cv2.inRange(hsv, lower_white, upper_white)
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for cnt in contours:
    if cv2.contourArea(cnt) > 100:
        (x, y, w, h) = cv2.boundingRect(cnt)
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        print(f"Репер найден на ({x}, {y})")

cv2.imshow("Detected", img)
cv2.waitKey(0)