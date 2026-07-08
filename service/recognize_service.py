import cv2
import numpy as np
import os
RECOGNIZER = cv2.face.LBPHFaceRecognizer_create()
PASS_CONF = 45
FACE_CASCADE = cv2.CascadeClassifier(os.getcwd() + '\\cascades\\haarcascade_frontalface_default.xml')

def train(pohots,lables):
    RECOGNIZER.train(pohots,np.array(lables))

def found_face(gray_img):
    faces = FACE_CASCADE.detectMultiScale(gray_img, 1.15, 4)
    return len(faces) > 0

def recognise_face(photo):
    label, confidence = RECOGNIZER.predict(photo)

    # print("识别结果：", label)
    # print("置信度：", confidence)

    if confidence > PASS_CONF:
        return -1

    return label
