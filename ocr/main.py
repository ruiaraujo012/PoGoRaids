#!/usr/bin/python3

import pytesseract
import sys
import cv2 as cv
import color
import re
import numpy as np

from PIL import Image

# TODO : adapt coordinates to scales
# TODO : fazer thresholds para diferentes toms no current time

# coords = (315, 445, 385, 470)


# img = cv.imread(sys.argv[1], 0)
# ret, thresh1 = cv.threshold(img, 215, 255, cv.THRESH_BINARY)
# # thresh1 = cv.adaptiveThreshold(
# #   img,  255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 125, 1)

# cv.imshow("threshold", thresh1)
# text = pytesseract.image_to_string(thresh1)

# print("Raw OCR")
# print(text)


# # Crop CP
# coords = (84, 117, 353, 185)
# # cropped_img_text = crop_image(thresh1, coords)

# # print("Time until start: " + cropped_img_text)


# cv.waitKey(0)
# cv.destroyAllWindows()


def percorrer_todas_raids():
    total_raids = 30

    for i in range(5, total_raids):
        file_name = "raids/raid_" + str(i) + ".jpg"
        extract(file_name)


def extract(img_path):
    img = cv.imread(img_path)

    # Convert image to grayscale
    # gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # Binary conversion
    # ret, thresh1 = cv.threshold(img, 185, 255, cv.THRESH_BINARY)
    # cv.imshow("threshold", thresh1)
    # text = pytesseract.image_to_string(thresh1)

    h, w, c = img.shape

    print("\n\n::::::::" + img_path + " :::::::: ")
    print("- Scale ("+str(w) + ","+str(h)+"): " + str(w/h))

    # scan_for_time_until_start(img)
    scan_for_current_time(img)


def scan_for_current_time(img):

    # Verificar 7.8.9 - aparecem a branco
    h, w, c = img.shape
    cropped = img[0:45, 0:w]
    gray = cv.cvtColor(cropped, cv.COLOR_BGR2GRAY)

    ret, thresh = cv.threshold(gray, 50, 255, cv.THRESH_BINARY_INV)

    # TODO : obter o delta e verificar que valores se recebe para tons de preto
    cor_atual = img[25, int(w/2)]
    preto = [0, 0, 0]
    delta = color.diff_between_rgb_colors(cor_atual[::1], preto)

    print("Cor atual {}, delta obtido {}".format(cor_atual, delta))

    # thresh1 = cv.adaptiveThreshold(
    #     gray,  255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 155, -1)

    cv.imshow("img", thresh)
    # cv.waitKey(0)
    # cv.destroyAllWindows()

    text = pytesseract.image_to_string(
        thresh, config='-c tessedit_char_whitelist=1234567890:~-AMP --psm 7')

    print("Current device time: {}".format(text))

    print("\n\nTeste Threshold")
    try_multiple_thresholds(gray)


def try_multiple_thresholds(gray_img):
    thresholds = [10, 25, 50, 100, 125, 150, 175, 200]

    for th in thresholds:
        print("Testing for thr {}".format(th))
        thresh = cv.resize(gray_img, None, fx=2, fy=2,
                           interpolation=cv.INTER_CUBIC)

        ret, thresh = cv.threshold(thresh, th, 255, cv.THRESH_BINARY_INV)

        cv.imshow("img", thresh)
        cv.waitKey(0)
        cv.destroyAllWindows()

        text = pytesseract.image_to_string(
            thresh, config='-c tessedit_char_whitelist=1234567890:~-AMP --psm 7')

        regex = re.findall(r'\d{1,2}:\d{2}', text)

        print("REGEX: {}".format(regex))

        if regex:
            hour, minute = regex[0].split(":")
            hour = int(hour)
            minute = int(minute)
            if hour > 0 and hour < 24 and minute > 0 and minute < 60:
                print("Deu match - {}".format(text))
                return text
            else:
                print("Falhou na procura de hora - {}".format(text))
        else:
            print("Falhou na procura de hora - {}".format(text))


def apply_threshold(img):

    h, w, c = img.shape
    color = img[1:1]
    print("Color no pixel {} e channel {}".format(color))


def scan_for_time_until_start(img):
    # 0.7627, 0.59973, 0.93220, 0.63342

    orange = [243, 121, 53]
    found_orange = False
    initial_orange_coords = []
    found_pixels = []
    count_orange_pixels = 0

    h, w, c = img.shape

    init_x = int(w * 0.65)
    init_y = int(h * 0.5)

    x = init_x
    y = init_y

    max_x = int(w*0.9)
    max_y = int(h*0.9)

    while(True):

        if x > max_x and y > max_y:
            break

        # print("Checking pixel {} {} c1{} c2{}".format(
        #     int(x), int(y), img[y, x], orange))

        # if x == 400 and y == 535:
        #     cv.imshow(img[y:y+200, x:x+250])
        #     cv.waitKey(0)
        #     cv.destroyAllWindows()

        if x < w - 25:
            x += 1
        else:
            x = init_x
            y += 1

        if count_orange_pixels > 85:

            min_x = 9999
            min_y = 9999
            max_x = -1
            max_y = -1

            section_max_height = 999
            for arr in found_pixels:
                if arr[1] < min_x:
                    min_x = arr[1]
                    initial_orange_coords = arr
                if arr[1] > max_x:
                    max_x = arr[1]

                if arr[0] < min_y:
                    min_y = arr[0]
                if arr[0] > max_y:
                    max_y = arr[0]

            top_left = [min_y, min_x]
            bot_right = [max_y, max_x]

            box_width = max_x - min_x
            box_height = max_y - min_y

            sec_x = initial_orange_coords[1]
            sec_y = initial_orange_coords[0]
            # print("Encontrou um bloco de laranjas com inicio em x.{} y.{}".format(
            #     sec_x, sec_y))

            time_section = img[sec_y:sec_y+33, sec_x:sec_x+box_width]
            gray = cv.cvtColor(time_section, cv.COLOR_BGR2GRAY)

            # Binary conversion
            ret, thresh1 = cv.threshold(
                gray, 200, 255, cv.THRESH_BINARY_INV)
            cv.imshow("threshold", thresh1)
            text = pytesseract.image_to_string(
                thresh1, config='-c tessedit_char_whitelist=1234567890:~-AMP --psm 7')

            regex = re.findall(r'\d{1,2}:\d{2}:\d{2}', text)

            if regex:
                print("Deu match no regex")
            else:
                print("No regex match")

            cv.waitKey(0)
            print("Time Until Start: {}".format(text))
            break

        # TODO : WARNING img[y,x] returns BGR instead of RGB
        if color.arbitrary_similarity(img[y, x][::-1], orange, 20):

            count_orange_pixels += 1
            # print("Color similar, total {}".format(count_orange_pixels))
            # print("C1{} C2{} x:{} y:{}".format(img[y, x], orange, x, y))

            found_pixels.append([y, x])

        else:
            count_orange_pixels = 0


def crop_image(img, coords, thresh_value):
    # [y:y+heightCut, x:x+widthCut]
    cropped = img[41:126, 16:533]
    cv.imshow("Cut image", cropped)
    text = pytesseract.image_to_string(
        cropped, config='-c tessedit_char_whitelist=1234567890:~-AMP --psm 7')
    return text


def main():
    percorrer_todas_raids()


main()
