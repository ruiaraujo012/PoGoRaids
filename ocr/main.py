#!/usr/bin/python3

import argparse
import logging
import datetime as dt
import cv2 as cv
from utils import process_img as pi
from utils import extractor as ex
from tests import ocr as test_ocr

logging.basicConfig(filename='example.log', level=logging.DEBUG)


def read_args():
    parser = argparse.ArgumentParser(description='Info to run main:')
    parser.add_argument('-i',
                        help='Name of screenshot with extension. Ex.: raid_1.jpg')
    parser.add_argument('-t',
                        help='Test all OCR images', action='store_true')
    parser.add_argument('-te',
                        help='Test OCR egg images', action='store_true')
    parser.add_argument('-tp',
                        help='Test OCR pokemon images', action='store_true')
    args = parser.parse_args()

    if args == None:
        print('Error! \nPlease use -h to see help')
    else:
        return(args)


def main():
    args = read_args()

    img_name = args.i
    test_ocr_eggs = args.te

    if test_ocr_eggs:
        test_ocr.test_ocr_eggs()

    if img_name != None:
        print("IMG NAME" + img_name)
        img = pi.read_image_egg(img_name)
        extracted_info = pi.process_img(img)

        print("EXTRACTED INFO")
        print(extracted_info)


main()
