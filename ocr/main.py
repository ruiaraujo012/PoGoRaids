#!/usr/bin/python3

import argparse
import logging
import cv2 as cv
from utils import process_img as pi
from utils import extractor as ex

logging.basicConfig(filename='example.log', level=logging.DEBUG)

f = open("results.txt", "w")


def read_args():
    parser = argparse.ArgumentParser(description='Info to run main:')
    parser.add_argument('-i',
                        help='Name of screenshot with extension. Ex.: raid_1.jpg')
    args = parser.parse_args()

    if args.i == None:
        print('Error! \nPlease use -h to see help')
    else:
        return(args.i)


def log_raid_data(name, phone_time, time_until_finish, did_egg_hatch, gym_name, level):

    data = "\n" + "=" * 15 + " Raid_" + name + " " + "=" * 15 + "\n"
    data += "Gym name: {}".format(gym_name) + "\n"
    data += "Level: {}".format(level) + "\n"
    data += "Phone time: {}".format(phone_time) + "\n"
    if did_egg_hatch:
        data += "Time until finish: {}".format(time_until_finish) + "\n"
    else:
        data += "Time to strart: {}".format(time_until_finish) + "\n"
    data += "Did egg hatch: {}".format(True if did_egg_hatch else False) + "\n"
    data += "="*40+"\n"

    print(data)
    f.write(data)


def main():
    img_name = read_args()
    if img_name != None:
        print('Image name: [{}]'.format(img_name))
        img = pi.read_image_pokemon(img_name)

        img_no_bottom = pi.remove_bottom_bar(img)
        croped_img = pi.crop_resize_img(img_no_bottom)

        phone_time, raid_time, did_egg_hatch = ex.extract(croped_img)

        level_img = pi.crop_raid_level(
            croped_img, did_egg_hatch)
        raid_level = ex.extract_level(level_img)

        # FIXME: Mudar isto depois do anterior estar corrigido
        if raid_level == 0:
            raid_level = 5

        coords = pi.detect_circles(img)

        if coords:
            # TODO: limpar o texto extraido do nome do ginasio
            gym_name = ex.extract_gym_name(img, coords)

        log_raid_data('raid', phone_time, raid_time,
                      did_egg_hatch, gym_name, raid_level)

        if did_egg_hatch:
            pokemon_name = pi.find_boss_name(croped_img, raid_level)

            if pokemon_name == None:
                print(' Error! '.center(40, '*'))
                print(" Can't read pokemon name! ".center(40, '*'))
                print(''.center(40, '*'))


main()
