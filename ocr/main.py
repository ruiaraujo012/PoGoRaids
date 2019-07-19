#!/usr/bin/python3

import pytesseract
import sys
import cv2 as cv
import color
import re
import numpy as np
import logging
import text_validation
import img_process

from PIL import Image

# TODO : adapt coordinates to scales

# NOTE : zoom in (cv.resize) parece ajudar em várias situacoes
# NOTE : teste a vários thresholds será menos eficiente mas muito mais consistente para diferentes cores, para zonas consistentes não vale a pena realizar esta operação ou então limitá-la a poucos testes

logging.basicConfig(filename='example.log', level=logging.DEBUG)


def percorrer_todas_raids():
    total_raids = 5

    for i in range(1, total_raids):
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

    # phone_time = scan_for_current_time(img)
    time_until_start = scan_for_time_until_start(img)

    print("\n\n========= Extracted data =========")
    # print("Phone time:       {}".format(phone_time))
    print("Time until start: {}".format(time_until_start))


def scan_for_current_time(img):

    # Verificar 7.8.9 - aparecem a branco
    h, w, c = img.shape
    cropped = img[0:45, 0:w]
    gray = cv.cvtColor(cropped, cv.COLOR_BGR2GRAY)
    zoomed = img_process.zoom_img(gray, 2, 2)

    ret, thresh = cv.threshold(zoomed, 50, 255, cv.THRESH_BINARY_INV)

    # TODO : reajustar estes valores
    thresholds = [10, 25, 50, 100, 125, 150, 175, 200]
    extracted_text = img_process.try_multiple_thresholds_ocr(
        zoomed, thresholds, text_validation.validate_hour_hh_mm)

    return extracted_text
    print("Extracted text {}".format(extracted_text))


def scan_for_time_until_start(img):

    orange = [243, 121, 53]
    time_until_start = img_process.section_by_color(img, orange,  [0.5, 0.65], [0.9, 0.9], 33, 0, [
    ], regex=text_validation.validate_hour_hh_mm_ss)

    # if not time_until_start:
    # Testar para o ROSA antes do hatch

    return time_until_start


def main():

    percorrer_todas_raids()
    cv.destroyAllWindows()


main()
