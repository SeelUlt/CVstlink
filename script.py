
import cv2
import numpy as np
import os
import shutil
from fileCounter import testfull
from fileCounter import testkey
from fileCounter import renamer
from fileCounter import renamer_with_counter
import grbl
from matplotlib import pyplot as plt
from grbl import streamCode

focus = 0.25
fixedFocus = False

#text parameters
#text = "Sample Text"
position = (10, 30)
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1.0
color = (0,256,256)
thickness = 2

def updater():

    image_path = 'tanya.jpg'  # замените на свой путь
    image = cv2.imread(image_path)

    # Преобразование в оттенки серого
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Удаление теней с помощью деления на структуру
    dilated_img = cv2.dilate(gray, np.ones((7, 7), np.uint8))
    bg_img = cv2.medianBlur(dilated_img, 21)
    diff_img = 255 - cv2.absdiff(gray, bg_img)
    norm_img = cv2.normalize(diff_img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)

    # Повышение контраста с использованием CLAHE
    clahe = cv2.createCLAHE(clipLimit=0.5, tileGridSize=(8, 8))
    enhanced = clahe.apply(norm_img)

    # Бинаризация изображения (черно-белое)
    _, binary = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Сохранение результата
    cv2.imwrite('enhanced_text_image.jpg', binary)

    # Отображение результата (опционально)
    cv2.imshow("Original", gray)
    cv2.imshow("Enhanced", binary)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    #полурабочий код с склейкой двух изображений
def stitcherella(image1, image2):
    # Загрузите изображения
    img1 = cv2.imread(image1)
    img2 = cv2.imread(image2)
    cv2.imshow("shower", img1)
    cv2.waitKey(0)
    cv2.imshow("shower", img2)
    cv2.waitKey(0)

    # Создайте объект Stitcher
    stitcher = cv2.Stitcher_create()
    status, stitched_image = stitcher.stitch([img1, img2,  cv2.imread('parts/3.jpeg')])

    if status == cv2.Stitcher_OK:
        cv2.imwrite('stitched_output.jpg', stitched_image)
        cv2.imshow('shower', stitched_image)
        cv2.waitKey(0)
        print("Изображения успешно склеены!")
    else:
        print("Ошибка склейки. Попробуйте вручную.")
    print(status)

def makePhoto(number, numberOfCamera, focus):
    cap = cv2.VideoCapture(numberOfCamera)
    cap.set(28, focus)
    for i in range(60):
        cap.read()
    ret, frame = cap.read()
    text = f"focus {focus}"
    cv2.putText(
        frame,
        text,
        position,
        font,
        font_scale,
        color,
        thickness
    )
    cv2.imwrite(f"originalScreens/frame{number}.png", frame,)
    cap.release()
    cv2.imshow("shower", frame)
def makePhotoCollection(number, numberOfCamera):
    focusValue = focus
    if number <= 0:
        return None
    else:
        for i in range(number):
            makePhoto(i, numberOfCamera, focusValue)
            if not fixedFocus:
                focusValue += 0.25

def blurFace(img):
    (h, w) = img.shape[:2]
    dW = int(w / 3)
    dH = int(h / 3)
    if dW % 2 == 0:
        dW -= 1
    if dH % 2 == 0:
        dH -= 1
    return cv2.GaussianBlur(img, (dW, dH), 0)

def camView():
    cam = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier('haarXML/haarcascade_frontalface_default.xml')
    while True:
        ret, img = cam.read()
        faces = face_cascade.detectMultiScale(img, scaleFactor=2, minNeighbors= 5, minSize = (20,20))
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)
            img[y:y+h, x:x+w] = blurFace(img[y:y+h, x:x+w])
        cv2.imshow("window", img)
        k = cv2.waitKey(10) & 0xFF
        if k == 27:
            break
    cam.release()
    cv2.destroyAllWindows()

def createDirectories():
    counter = 1238
    end = 1251
    while counter < end:
        os.makedirs(f"greenTest/perfects/{counter}", exist_ok=True)
        counter+=1

#streamCode("COM1", "/gcode/test0.gcode")
#camView()
#createDirectories()

# i = testkey('greenTest/perfects', 'IMG')
# j = testkey('greenTest/perfects', '.jpeg')
# print(j-i)

#renamer('greentest/perfects/1244', 'IMG', 'копия')
# camView()
#
# # Путь к директории
# basepath = 'greenTest/perfects'
# directories = os.listdir(basepath)
#
# for folder in directories:
#     folderpath = os.path.join(basepath, folder)
#     if os.path.isdir(folderpath):
#         for entry in os.scandir(folderpath):
#             if 'positive' in entry.name:
#                 shutil.copy(entry.path, 'greenTest/positives')
# shutil.copy('greenTest/perfects/1234/positive107.jpeg', 'greenTest/positives')

# renamer_with_counter("greenTest/negatives", "negative", "jpeg")
