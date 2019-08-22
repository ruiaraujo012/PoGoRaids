#!/usr/bin/python3

import argparse
import logging
import json
from utils import process_img as pi
from tests import ocr as test_ocr
from packages import pokestop as pk

logging.basicConfig(filename='example.log', level=logging.DEBUG)


def read_args():
    """ Get args that is needed in script. """
    parser = argparse.ArgumentParser(description='Info to run main:')
    parser.add_argument('-i',
                        help='Name of screenshot with extension. Ex.: raid_1.jpg')
    parser.add_argument('-t',
                        help='Test OCR images', action='store_true')
    parser.add_argument('-lat', dest='latitude',
                        help='Latitude for portals request')
    parser.add_argument('-lon', dest='longitude',
                        help='Longitude for portals request')
    parser.add_argument('-guid', dest='guid',
                        help='Portal id to get information')
    args = parser.parse_args()

    if args is None:
        print('Error! \nPlease use -h to see help')

    return(args)


def main():
    """ Main function. """
    args = read_args()

    img_name = args.i
    test_ocr_eggs = args.t

    if test_ocr_eggs:
        test_ocr.test_ocr()

    if img_name is not None:
        print("IMG NAME {}".format(img_name))
        img = pi.read_image(img_name)

        portals = None

        if args.guid:
            portals = pk.main2(guid=args.guid)
            portals = json.loads(portals)
        elif args.latitude and args.longitude:
            portals = pk.main2(latitude=args.latitude,
                               longitude=args.longitude)
            portals = json.loads(portals)

        extracted_info = pi.process_img(img, portals)

        print("EXTRACTED INFO: \n{}".format(extracted_info))


main()
