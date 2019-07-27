#!/usr/bin/python3


import pytesseract
from pytesseract import Output
import sys
import cv2 as cv
import color
import re
import numpy as np
import math
import logging
import text_validation
import img_process
import pokemon_name as pn
import statistics
import imutils
from matplotlib import pyplot as plt


from PIL import Image

# TODO : adapt coordinates to scales

# NOTE : zoom in (cv.resize) parece ajudar em várias situacoes
# NOTE : teste a vários thresholds será menos eficiente mas muito mais consistente para diferentes cores, para zonas consistentes não vale a pena realizar esta operação ou então limitá-la a poucos testes

logging.basicConfig(filename='example.log', level=logging.DEBUG)

f = open("results.txt", "w")


def percorrer_todas_raids():
    total_raids = 35

    for i in range(1, total_raids):

        img_path = "raids/pokemon/" + str(i) + ".jpg"
        img = cv.imread(img_path)

        phone_time, time_until_start, did_egg_hatch = extract(img)

        level = extract_level(img_path)
        coords = detect_circles(img)

        if not coords:
            continue

        w, h, c = img.shape

        # print("Coords {}".format(coords))

        img = img[coords[0]-coords[2]:coords[0] +
                  coords[2], coords[1]+coords[2]:w]

        img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
        ret, img = cv.threshold(img,
                                205, 255, cv.THRESH_BINARY_INV)

        text = pytesseract.image_to_string(
            img, config='--psm 6')

        log_raid_data(str(i), phone_time, time_until_start, did_egg_hatch)


def log_raid_data(name, phone_time, time_until_start, did_egg_hatch):

    data = "=" * 11 + " Raid_" + name + " " + "=" * 11 + "\n"
    data += "Phone time: {}".format(phone_time) + "\n"
    data += "Time until start: {}".format(time_until_start) + "\n"
    data += "Did egg hatch: {}".format(True if did_egg_hatch else False) + "\n"
    data += "="*30+"\n\n" + "\n\n"

    print(data)
    f.write(data)


def detect_circles(img):

    output = img.copy()
    gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

    # detect circles in the image
    circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT,
                              2, 150,  minRadius=25, maxRadius=100)

    image_circle = None
    # ensure at least some circles were found
    if circles is not None:
        # convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")

        min_x = 9999
        min_y = 9999
        # loop over the (x, y) coordinates and radius of the circles
        for (x, y, r) in circles:
            # draw the circle in the output image, then draw a rectangle
            # corresponding to the center of the circle
            cv.circle(output, (x, y), r, (0, 255, 0), 4)
            cv.rectangle(output, (x - 5, y - 5),
                         (x + 5, y + 5), (0, 128, 255), -1)

            if x < min_x and y < min_y:
                min_x = x
                min_y = y
                image_circle = (min_y, min_x, r)

        # show the output image
        # cv.imshow("output", np.hstack([img, output]))
        # cv.waitKey(0)

    return image_circle


def extract_level(img_path):
    img_rgb = cv.imread(img_path)

    # img_rgb = cv.imrad('image.png')
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    template = cv.imread('raid_icon_cut_2.png', 0)
    template = cv.resize(template, None, fx=0.25,
                         fy=0.25, interpolation=cv.INTER_CUBIC)

    loc = [[]]
    level = 0
    while(True):
        w, h = template.shape[::-1]

        if w < 25 and h < 25:
            break

        # print(w, h)
        # TODO: analizar os elemtnos q se sobrepoem

        # TM_CCOEFF_NORMED
        res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
        threshold = 0.65
        loc = np.where(res >= threshold)

        # print(loc)
        x_dist = 0
        for pt in zip(*loc[::-1]):
            cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

            # cv.imshow('res.png', img_rgb)

        for (index, point) in enumerate(loc[1][:-1]):
            diff = abs(loc[1][index + 1] - point)
            if diff > w:
                level += 1

        if(len(loc[0]) > 0):

            # cv.imshow("output", img_rgb)
            # cv.imshow("output2", template)
            # cv.waitKey(0)
            print("Level {}".format(level))

        template = cv.resize(template, None, fx=0.98,
                             fy=0.98, interpolation=cv.INTER_CUBIC)


def extract(img):
    h, w, c = img.shape

    phone_time = scan_for_current_time(img)
    time_until_start, did_egg_hatch = scan_for_time_until_start(img)

    return phone_time, time_until_start, did_egg_hatch


def section_cut(img, name):
    h, w, c = img.shape
    imgray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    w_scale = w/1080
    h_scale = h/2160

    img = imutils.resize(img, height=2160)

    print("Scale ({}, {}) {} {}".format(h, w, w_scale, h_scale))

    # mobile bar
    mobile_bar = img[0:min(int(55*h_scale), 55), 0: w]

    before_hatch = img.copy()

    # before_hatch
    before_hatch = before_hatch[int(450*h_scale):int(620*h_scale),
                                int(340*w_scale):int(750*w_scale)]

    level_before_hatch = img[int(
        650*h_scale): int(755*h_scale), int(255*w_scale): int(870*w_scale)]

    level_after_hatch = img[int(
        315*h_scale): int(390*h_scale), int(255*w_scale): int(870*w_scale)]

    pokemon = img[int(572*h_scale): int(723*h_scale),
                  int(180*w_scale): int(930*w_scale)]

    timer_after_hatch = img[int(
        1255*h_scale): int(1380*h_scale), int(760*w_scale): int(1028*w_scale)]

    cv.imwrite("{}_{}.jpg".format(name, "mobile"), mobile_bar)
    cv.imwrite("{}_{}.jpg".format(name, "before_hatch"), before_hatch)
    cv.imwrite("{}_{}.jpg".format(
        name, "level_before_hatch"), level_before_hatch)
    cv.imwrite("{}_{}.jpg".format(
        name, "level_after_hatch"), level_after_hatch)
    cv.imwrite("{}_{}.jpg".format(name, "pokemon"), pokemon)
    cv.imwrite("{}_{}.jpg".format(
        name, "timer_after_hatch"), timer_after_hatch)


def scan_for_pokemon_name(img):
    h, w, c = img.shape
    cropped = img[int(h*0.24):int(h*0.34), int(w*0.23):int(w*0.75)]
    gray = cv.cvtColor(cropped, cv.COLOR_BGR2GRAY)
    zoomed = img_process.zoom_img(gray, 2, 2)
    # ret, thresh = cv.threshold(zoomed, 200, 255, cv.THRESH_BINARY_INV)
    thresholds = [225, 230, 240, 245, 200, 190, 180, 165]
    img_process.try_multiple_thresholds_pokemon_name(zoomed, thresholds)

    # Fuzzy finder to compare with pokemon names


def scan_for_current_time(img):

    # Verificar 7.8.9 - aparecem a branco
    h, w, c = img.shape
    vscale = h/960
    cropped = img[0:min(int(45*vscale), 65), 0:w]
    gray = cv.cvtColor(cropped, cv.COLOR_BGR2GRAY)
    zoomed = img_process.zoom_img(gray, 2, 2)

    ret, thresh = cv.threshold(zoomed, 50, 255, cv.THRESH_BINARY_INV)

    # TODO : reajustar estes valores
    thresholds = [190, 200, 210, 165, 150, 130, 100, 85, 50, 25]
    extracted_text = img_process.try_multiple_thresholds_ocr(
        zoomed, thresholds, text_validation.validate_hour_hh_mm)

    return extracted_text
    print("Extracted text {}".format(extracted_text))


def scan_for_time_until_start(img):

    orange = [243, 121, 53]
    time_until_start = img_process.section_by_color(img, orange,  [0.5, 0.65], [0.8, 0.99], 34, 0, [
    ], regex=text_validation.validate_hour_hh_mm_ss)
    did_egg_hatch = True

    if not time_until_start:
        print("Testing timer before hatch")
        pink = [243, 136, 142]
        time_until_start = img_process.section_by_color(img, pink,  [0.15, 0.2], [0.45, 0.85], 50, 0, [
        ], pixels_quantity=150, regex=text_validation.validate_hour_hh_mm_ss)
        did_egg_hatch = False

    return time_until_start, did_egg_hatch


def main():
    screenshot_name = 0
    raid_level = 5
    pn.find_boss_name_from_screenshot(screenshot_name, raid_level)
    percorrer_todas_raids()


main()
