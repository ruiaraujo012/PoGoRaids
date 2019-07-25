#!/usr/bin/python3

import argparse
import math
import cv2 as cv
from matplotlib import pyplot as plt
import pytesseract
import img_process

# parser = argparse.ArgumentParser(description='Name of screenshot.')
# parser.add_argument('--num', type=int, default=1,
#                     help='an integer for the path screen')

# args = parser.parse_args()

# img = cv.imread('raids/raid_' + str(args.num) + '.jpg')

total_raids = 36

for i in range(1, total_raids):
    img_path = "raids/raid_" + str(i) + ".jpg"

    img = cv.imread(img_path)

    h, w, c = img.shape

    print('Resolution size: {} x {}'.format(h, w))

    width = 900
    crop_img = img[0:int(h/3*2), 0:w]

    imgScale = width/w

    newX = img.shape[1]*imgScale

    resize_img = cv.resize(crop_img, (int(newX), 960))

    cv.rectangle(resize_img, (650, 850), (650 + 200, 850 + 50), (0, 255, 0), 5)

    h_r, w_r, c_r = resize_img.shape

    # cv.rectangle(resize_img, (int(w_r * 0.1), 340),(int(w_r * 0.9), 340 + 120), (0, 0, 255), 5)

    crop_crop_img = resize_img[340:460, int(w_r * 0.1):int(w_r * 0.9)]

    gray = cv.cvtColor(crop_crop_img, cv.COLOR_BGR2GRAY)

    ret, thresh = cv.threshold(
        gray, 240, 255, cv.THRESH_BINARY_INV)

    kernel = cv.getStructuringElement(cv.MORPH_RECT, (4, 8))
    morph_img = cv.morphologyEx(thresh, cv.MORPH_CLOSE, kernel)

    text = pytesseract.image_to_string(
        thresh, config='--psm 7 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyz')

    print("Pokemon name: {}".format(text))

    cv.imshow('test', morph_img)
    cv.waitKey(0)
    cv.destroyAllWindows()
