import json
import datetime as dt
from utils import process_img as pi
from utils import log

f = open("tests.txt", "w", encoding="utf-8")


def test_ocr():

    with open('./ocr-python/data/test_ocr.json', encoding="utf-8") as json_file:
        imgs = json.load(json_file)

        for row in imgs:
            img = pi.read_image(row['img'])
            phone_time, raid_time, did_egg_hatch, gym_name, level, pokemon, raid_hour = pi.process_img(
                img)
            log.log_raid_data(row['img'], phone_time, raid_time,
                              did_egg_hatch, gym_name, level, pokemon)

            validate_data(row['img'], phone_time, raid_time,
                          did_egg_hatch, gym_name, level, pokemon, row)


def validate_data(name, phone_time, raid_time, did_egg_hatch, gym_name, level, pokemon, data):

    info = "=" * 20 + " " + name + " " + "=" * 20 + "\n"

    if(data['gym_name'].strip().lower() != gym_name.strip().lower()):
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

    if 'time_until_start' in data:
        try:
            if(dt.datetime.strptime(data['time_until_start'], '%H:%M:%S') != dt.datetime.strptime(raid_time, '%H:%M:%S')):
                info += "Invalid time until start, expected {}, result: {} \n".format(
                    data['time_until_start'], raid_time)
        except:
            info += "Invalid time until start, expected {}, result: {} \n".format(
                    data['time_until_start'], raid_time)

    elif 'time_until_finish' in data:
        try:
            if(dt.datetime.strptime(data['time_until_finish'], '%H:%M:%S') != dt.datetime.strptime(raid_time, '%H:%M:%S')):
                info += "Invalid time until start, expected {}, result: {} \n".format(
                    data['time_until_start'], raid_time)
        except:
            info += "Invalid time until finish, expected {}, result: {} \n".format(
                data['time_until_start'], raid_time)

    if(data['level'] != level):
        info += "Invalid level, expected {}, result: {} \n".format(
            data['level'], level)

    if(pokemon in data and data['pokemon'].lower() != pokemon.lower()):
        info += "Invalid pokemon, expected {}, result: {} \n".format(
            data['pokemon'], pokemon)

    if(len(info.split("\n")) > 2):
        f.write(info + "\n")
        print(str(info + "\n").encode("utf-8"))
    else:
        success_message = "==> {} passed all tests \n".format(name)
        print(success_message.encode("utf-8"))
        f.write(success_message)
