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
import statistics
import imutils
from matplotlib import pyplot as plt


from PIL import Image

# TODO : adapt coordinates to scales

# NOTE : zoom in (cv.resize) parece ajudar em várias situacoes
# NOTE : teste a vários thresholds será menos eficiente mas muito mais consistente para diferentes cores, para zonas consistentes não vale a pena realizar esta operação ou então limitá-la a poucos testes

logging.basicConfig(filename='example.log', level=logging.DEBUG)


def percorrer_todas_raids():
    total_raids = 30

    for i in range(1, total_raids):
        img_path = "raids/raid_" + str(i) + ".jpg"
        name = str(i) + "_"
        # extract(img_path, name)
        # captch_ex(img_path)
        img = cv.imread(img_path)
        # img_to_boxes(img)
        # extract_level(img)
        coords = detect_circles(img)

        if not coords:
            continue

        w, h, c = img.shape

        print("Coords {}".format(coords))

        img = img[coords[0]-coords[2]:coords[0] +
                  coords[2], coords[1]+coords[2]:w]

        img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
        ret, img = cv.threshold(img,
                                205, 255, cv.THRESH_BINARY_INV)

        text = pytesseract.image_to_string(
            img, config='--psm 6')

        print("Extracted text {}".format(text))

        cv.imshow("img", img)
        cv.waitKey(0)


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
        cv.imshow("output", np.hstack([img, output]))
        cv.waitKey(0)

    return image_circle


def ex2(img_path):
    img_rgb = cv.imread(img_path)
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    template = cv.imread('raid_icon_2.png', 0)
    w, h = template.shape[::-1]
    res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
    threshold = 0.75
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
    cv.imshow('res.png', img_rgb)
    cv.waitKey(0)


def extract_level(img):
    img_rgb_org = img
    img_gray_org = cv.cvtColor(img_rgb_org, cv.COLOR_BGR2GRAY)
    template = cv.imread('raid_icon_2.png')
    img_gray_org = img_gray_org[150:700, 400:1750]
    w, h, c = template.shape  # [::-1]
    template = cv.cvtColor(template, cv.COLOR_BGR2GRAY)
    template = template[250:1100, 30:900]

    cv.imshow("te", img_gray_org)
    cv.waitKey(0)

    methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
               'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']

    for meth in methods:
        img_gray = img_gray_org.copy()
        img_rgb = img_rgb_org.copy()
        res = cv.matchTemplate(img_gray, template, eval(meth))
        threshold = 0.8
        loc = np.where(res >= threshold)
        print(loc)
        for pt in zip(*loc[::-1]):
            cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

        img_rgb = cv.resize(img_rgb, None, fx=0.5, fy=0.5,
                            interpolation=cv.INTER_CUBIC)
        cv.imshow("level", img_rgb)
        cv.waitKey(0)


def extract(img_path, name):
    img = cv.imread(img_path)
    h, w, c = img.shape

    print("\n\n::::::::" + img_path + " :::::::: ")
    # print("- Scale ({},{}): ".format(str(w), str(h), str(w/h)))

    # cut = section_cut(img, name)

    # pre_process_image_2(img, name)

    # f = cv.createBackgroundSubtractorKNN()
    # mask = f.apply(img)

    # cv.imshow("mask", mask)
    # cv.waitKey(0)

    phone_time = scan_for_current_time(img)
    time_until_start, did_egg_hatch = scan_for_time_until_start(img)
    # if did_egg_hatch:
    #     scan_for_pokemon_name(img)

    print("Phone time: {}".format(phone_time))
    print("Time until start: {}".format(time_until_start))
    print("\n\n\n")


def img_to_boxes(img):
    img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
    d = pytesseract.image_to_data(img, output_type=Output.DICT)

    print(pytesseract.image_to_boxes(img))

    n_boxes = len(d['level'])
    for i in range(n_boxes):
        (x, y, w, h) = (d['left'][i], d['top']
                        [i], d['width'][i], d['height'][i])
    print("PRINTING")
    cv.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv.imshow('img', img)
    cv.waitKey(0)


def captch_ex(file_name):
    img = cv.imread(file_name)

    img_final = cv.imread(file_name)
    img_final = img_process.zoom_img(img_final, 2, 2)
    img = img_process.zoom_img(img, 2, 2)
    img2gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    ret, mask = cv.threshold(img2gray, 215, 255, cv.THRESH_BINARY)
    cv.imshow("mask", mask)
    cv.waitKey(0)
    image_final = cv.bitwise_and(img2gray, img2gray, mask=mask)
    # for black text , cv.THRESH_BINARY_INV
    ret, new_img = cv.threshold(image_final, 180, 255, cv.THRESH_BINARY)
    '''
            line  8 to 12  : Remove noisy portion 
    '''
    kernel = cv.getStructuringElement(cv.MORPH_CROSS, (3,
                                                       3))  # to manipulate the orientation of dilution , large x means horizonatally dilating  more, large y means vertically dilating more
    # dilate , more the iteration more the dilation
    dilated = cv.dilate(new_img, kernel, iterations=9)

    # for cv2.x.x

    # findContours returns 3 variables for getting contours
    contours, hierarchy = cv.findContours(
        dilated, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

    # for cv3.x.x comment above line and uncomment line below

    #image, contours, hierarchy = cv2.findContours(dilated,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    for contour in contours:
        # get rectangle bounding contour
        [x, y, w, h] = cv.boundingRect(contour)

        # Don't plot small false positives that aren't text
        if w < 15 and h < 15:
            continue

        # draw rectangle around contour on original image
        cv.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 2)

        '''
        #you can crop image and send to OCR  , false detected will return no text :)
        cropped = img_final[y :y +  h , x : x + w]

        s = file_name + '/crop_' + str(index) + '.jpg' 
        cv2.imwrite(s , cropped)
        index = index + 1

        '''
    # write original image with added contours to disk
    cv.imshow('captcha_result', img)
    cv.waitKey()

    cv.imwrite("cp_"+file_name, img)

    cv.imwrite('captcha.jpg', img)


def pre_process_image_2(img, name):
    gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
    cv.imshow("img", img)
    cv.waitKey(0)

    ret, thresh = cv.threshold(gray, 215, 255, cv.THRESH_BINARY)
    cv.imshow("gray", thresh)
    cv.waitKey(0)

    h, w, _ = img.shape
    asd = 0
    cinza = 170
    dentro = False
    # for x in range(w):
    #     for y in range(h):
    #         if gray[y, x] > 235:
    #             # print([gray[y, x]])
    #             gray[y, x] = 0
    #         asd += 1
    #         something = img[y, x]

    print(gray[400, 100])
    print(gray[415, 380])
    print("Cinza {}".format(gray[400, 366]))
    cv.imshow("img", gray)
    cv.waitKey(0)

    print(asd)
    cv.imwrite("gray.jpg", gray)
    # print(gray[y, x])


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


def pre_process_image(img):
    h, w, c = img.shape
    max_y = 0

    moda = []
    coords = None
    for x in range(0, 1):
        contiguous_pixels = 0
        for y in range(0, 55):

            similarity_black = color.diff_between_rgb_colors(
                img[y, x][::-1], [0, 0, 0])
            similarity_white = color.diff_between_rgb_colors(
                img[y, x][::-1], [255, 255, 255])

            print("({}, {}) - Color: {} , bl {} , wh {}".format(x,
                                                                y, img[y, x], similarity_black, similarity_white))

            # if similarity_white < 22 or similarity_black < 22:
            #     moda.append(y)
            #     if y > max_y:
            #         max_y = y
            #         contiguous_pixels += 1
            #         coords = (x, y)

    # print("Moda : {}".format(statistics.mean(moda)))
    # print("Nas coordenadas {}".format(coords))
    # print("Topbar Size: {}".format(max_y))
    # cropped = img[0:int(statistics.mean(moda)), 0:w]
    cv.imshow("img", img)
    cv.waitKey(0)
    cv.destroyAllWindows()


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

    percorrer_todas_raids()
    # captch_ex()
    cv.destroyAllWindows()


main()
