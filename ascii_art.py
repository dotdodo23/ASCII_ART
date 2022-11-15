import cv2 as cv
import numpy as np
import sys, os
from time import time_ns
from math import ceil

def imgprint(img):
    os.system('cls')
    for i in range(len(img)):
        for j in range(len(img[i])):
            sys.stdout.write("%c" % img[i][j])
        sys.stdout.write("\n")

def img_to_ascii(img: np.ndarray, scale: float = 1) -> np.ndarray:
    height, width = img.shape[:2]
    scale = 1/scale
    height = int(height//(16*scale))
    width = int(width//(7*scale))
    if img.ndim == 3: img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    ascii = np.array([ord(' '), ord('-'), ord('+'), ord('#'), ord('0')])
    devide = ceil(256/len(ascii))
    img = cv.resize(img,(width,height), interpolation = cv.INTER_AREA)
    _img = np.zeros_like(img)
    _img = ascii[img//devide]
    return _img

def video_to_ascii(src):
    cap = cv.VideoCapture(src)
    fps = cap.get(cv.CAP_PROP_FPS)
    f_time = 1000000000/(fps)
    next_time = time_ns()
    nframe = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            if nframe == 0:
                print("Can't receive frame. Exiting ...")
            else:
                print("stream end. Exiting ...")
            break
        nframe += 1
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        tmp = img_to_ascii(gray, 1)
        while (next_time - time_ns())>=0:
            pass
        next_time += f_time
        os.system('cls')
        for i in tmp:
            for j in i:
                sys.stdout.write('%c' % chr(j))
            sys.stdout.write('\n')
        cv.waitKey(0)
    cap.release()


video_to_ascii('ba.webm')
