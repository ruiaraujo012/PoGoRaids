import json
import datetime as dt
from utils import process_img as pi
from utils import log

f = open("tests.txt", "w")


def test_ocr_eggs():

    with open('data/test_eggs.json') as egg:
        imgs = json.load(egg)
        # print(imgs)

        for egg_img in imgs:
            img = pi.read_image_egg(egg_img['img'])
            phone_time, time_until_start, did_egg_hatch, gym_name, level, pokemon = pi.process_img(
                img)
            log.log_raid_data(egg_img['img'], phone_time, time_until_start,
                              did_egg_hatch, gym_name, level, pokemon)

            validate_data(egg_img['img'], phone_time, time_until_start,
                          did_egg_hatch, gym_name, level, pokemon, egg_img)


def validate_data(name, phone_time, time_until_start, did_egg_hatch, gym_name, level, pokemon, data):

    info = "=" * 20 + " " + name + " " + "=" * 20 + "\n"

    if(data['gym_name'].strip() != gym_name.strip()):
        info += "Invalid gym name, expected: {}, result: {} \n".format(
            data['gym_name'], gym_name)

    # TODO: Ter em atenção os telemóveis que apresentam segundos, poderá gerar erro na conversão?!
    try:
        if(dt.datetime.strptime(data['mobile_time'], '%H:%M') != dt.datetime.strptime(phone_time, '%H:%M')):
            info += "Invalid phone time, expected {}, result: {} \n".format(
                data['mobile_time'], phone_time)
    except:
        info += "Invalid phone time, expected {}, result: {} \n".format(
            data['mobile_time'], phone_time)

    try:
        if(dt.datetime.strptime(data['time_until_start'], '%H:%M:%S') != dt.datetime.strptime(time_until_start, '%H:%M:%S')):
            info += "Invalid time until start, expected {}, result: {} \n".format(
                data['time_until_start'], time_until_start)
    except:
        info += "Invalid time until start, expected {}, result: {} \n".format(
            data['time_until_start'], time_until_start)

    if(data['level'] != level):
        info += "Invalid level, expected {}, result: {} \n".format(
            data['level'], level)

    if(len(info.split("\n")) > 1):
        f.write(info)
        print(info)
    else:
        success_message = "==> {} passed all tests".format(name)
        print(success_message)
        f.write(success_message)
