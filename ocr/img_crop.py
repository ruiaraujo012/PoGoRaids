#!/usr/bin/python3


import img_process
import pytesseract
from matplotlib import pyplot as plt
import cv2 as cv
import math
import argparse
from utils.process_img import *
import color as co

# parser = argparse.ArgumentParser(description='Name of screenshot.')
# parser.add_argument('--num', type=int, default=1,
#                     help='an integer for the path screen')

# args = parser.parse_args()

# img = cv.imread('raids/raid_' + str(args.num) + '.jpg')

total_raids = 35

for i in range(1, total_raids):
    img_path = "raids/raid_" + str(i) + ".jpg"

    img = cv.imread(img_path)

    h, w, c = img.shape
    print("Prev size {} {}".format(h, w))
    color = img[h-1, 0]

    is_black = co.diff_between_rgb_colors(color[::-1], [0, 0, 0]) < 10
    is_white = co.diff_between_rgb_colors(color[::-1], [255, 255, 255]) < 10
    is_orange = co.diff_between_rgb_colors(color[::-1], [245, 80, 32]) < 10

    cv.imshow("prev image", img)
    cv.waitKey(0)

    print("Color initial {} {}".format(
        color, co.diff_between_rgb_colors(color, img[h-2, 0])))

    if is_black or is_white or is_orange:
        pixel_cut = 0
        while(co.diff_between_rgb_colors(color, img[h-1, 0]) < 5):
            pixel_cut += 1
            h -= 1
            print("{} {}".format(
                h, co.diff_between_rgb_colors(color, img[h, 0])))

        if pixel_cut > 25:
            img = img[0:h, 0:w]
            print("New size {} {}".format(h, w))
            cv.imshow("new image", img)
            cv.waitKey(0)

        h, w, c = img.shape

        print('Resolution size: {} x {}'.format(h, w))

    width = 900
    crop_img = img[0:int(h/3*2), 0:w]

# for i in range(1, total_raids):
#     img = read_image(i)

#     processed_img = crop_resize_img(img)

#     # cv.rectangle(processed_img, (650, 850),
#     #              (650 + 200, 850 + 50), (0, 255, 0), 5)

#     # cv.rectangle(resize_img, (int(w_r * 0.1), 340),(int(w_r * 0.9), 340 + 120), (0, 0, 255), 5)

#     pokemon_name_img = crop_pokemon_name(processed_img)

#     thresh = get_threshold(pokemon_name_img, 240, True)

#     text = pytesseract.image_to_string(
#         thresh, config='--psm 7 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyz')

#     print("Pokemon name: {}".format(text))

#     cv.imshow('test', thresh)
#     cv.waitKey(0)
#     cv.destroyAllWindows()
