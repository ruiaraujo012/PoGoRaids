f = open("results.txt", "w", encoding="utf-8")


def log_raid_data(name, phone_time, time_until_finish, did_egg_hatch, gym_name, level, pokemon):

    data = "\n" + "=" * 15 + " Raid_" + name + " " + "=" * 15 + "\n"
    data += "Gym name: {}".format(gym_name) + "\n"
    data += "Pokemon: {}".format(pokemon) + "\n"
    data += "Level: {}".format(level) + "\n"
    data += "Phone time: {}".format(phone_time) + "\n"
    if did_egg_hatch:
        data += "Time until finish: {}".format(time_until_finish) + "\n"
    else:
        data += "Time to strart: {}".format(time_until_finish) + "\n"
    data += "Did egg hatch: {}".format(True if did_egg_hatch else False) + "\n"
    data += "="*40+"\n"

    print(data.encode("utf-8"))
    f.write(data)

    return data
