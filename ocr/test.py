#!/usr/bin/python3

import argparse
import cv2 as cv
from utils import process_img as pi
from utils import extractor as ex


def read_args():
    parser = argparse.ArgumentParser(description='Info to run main:')
    parser.add_argument('-i',
                        help='Name of screenshot with extension. Ex.: raid_1.jpg')
    args = parser.parse_args()

    if args.i == None:
        print('Error! \nPlease use -h to see help')
        return None
    else:
        return(args.i)


def try_percentage(img, raid_hatched, have_bottom):
    h, w, c = img.shape

    if raid_hatched:
        if have_bottom:
            crop_img = img[200:260, int(w * 0.3):int(w * 0.7)]
        else:
            crop_img = img[200:260, int(w * 0.3):int(w * 0.7)]
    else:
        if have_bottom:
            crop_img = img[int(h * 0.25):int(h * 0.25),
                           int(w * 0.25):int(w * 0.75)]
            cv.imshow('cropb', crop_img)
            cv.waitKey(0)
        else:
            crop_img = img[int(h * 0.25):int(h * 0.35),
                           int(w * 0.25):int(w * 0.75)]
            cv.imshow('cropnb', crop_img)
            cv.waitKey(0)

    return crop_img


def main():
    img_name = read_args()
    if img_name != None:
        print('Image name: [{}]'.format(img_name))
        img = pi.read_image_pokemon(img_name)

        h, w, c = img.shape

        phone_time, time_until_finish, did_egg_hatch = ex.extract(img)

        img_no_bottom, have_bottom_bar = pi.remove_bottom_bar(img)

        new_img = cv.resize(img_no_bottom, (w, h))

        try_percentage(img_no_bottom, did_egg_hatch, have_bottom_bar)

        # cv.imshow('t', new_img)
        # cv.waitKey(0)

        # croped_img = pi.crop_resize_img(img_no_bottom)
        # level_img = pi.crop_raid_level(
        #     croped_img, did_egg_hatch, have_bottom_bar)
        # raid_level = ex.extract_level(level_img)


main()
