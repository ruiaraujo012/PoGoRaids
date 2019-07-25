#!/usr/bin/python3


import img_process
import pytesseract
from matplotlib import pyplot as plt
import cv2 as cv
import math
import argparse
from utils.process_img import *

# parser = argparse.ArgumentParser(description='Name of screenshot.')
# parser.add_argument('--num', type=int, default=1,
#                     help='an integer for the path screen')

# args = parser.parse_args()

# img = cv.imread('raids/raid_' + str(args.num) + '.jpg')

total_raids = 35


for i in range(1, total_raids):
    img = read_image(i)

    processed_img = crop_resize_img(img)

    # cv.rectangle(processed_img, (650, 850),
    #              (650 + 200, 850 + 50), (0, 255, 0), 5)

    # cv.rectangle(resize_img, (int(w_r * 0.1), 340),(int(w_r * 0.9), 340 + 120), (0, 0, 255), 5)

    pokemon_name_img = crop_pokemon_name(processed_img)

    thresh = get_threshold(pokemon_name_img, 240, True)

    text = pytesseract.image_to_string(
        thresh, config='--psm 7 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyz')

    print("Pokemon name: {}".format(text))

    cv.imshow('test', thresh)
    cv.waitKey(0)
    cv.destroyAllWindows()
