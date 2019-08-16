#!/usr/bin/python3

import argparse
import logging
import datetime as dt
import json
from utils import process_img as pi
from utils import extractor as ex
from tests import ocr as test_ocr

logging.basicConfig(filename='example.log', level=logging.DEBUG)


def read_args():
    parser = argparse.ArgumentParser(description='Info to run main:')
    parser.add_argument('-i',
                        help='Name of screenshot with extension. Ex.: raid_1.jpg')
    parser.add_argument('-t',
                        help='Test OCR images', action='store_true')
    args = parser.parse_args()

    if args == None:
        print('Error! \nPlease use -h to see help')
    else:
        return(args)


def main():
    args = read_args()

    img_name = args.i
    test_ocr_eggs = args.t

    if test_ocr_eggs:
        test_ocr.test_ocr()

    print("This is a test")

    if img_name is not None:
        img = pi.read_image(img_name)
        extracted_info = pi.process_img(img)

        print("Extracted info")
        print(extracted_info)

        extracted_info = {
            'gym_name': extracted_info.gym_name,
            'raid_level': extracted_info.raid_level,
            'raid_hour': extracted_info.raid_hour,
            'pokemon': extracted_info.pokemon_name,
            'did_egg_hatch': extracted_info.did_egg_hatch,
            'phone_time': extracted_info.phone_time,
            'raid_time': extracted_info.raid_time
        }

        print("This is a test")
        print(json.dumps(extracted_info))


main()
