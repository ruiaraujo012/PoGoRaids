import re


def validate_hour_hh_mm(text):
    regex = re.findall(r'\d{1,2}:\d{2}', text)

    print("REGEX: {}".format(regex))

    if regex:
        hour, minute = regex[0].split(":")
        hour = int(hour)
        minute = int(minute)
        if hour >= 0 and hour < 24 and minute >= 0 and minute < 60:
            print("Deu match - {}".format(text))
            return regex[0].strip()
        else:
            print("Falhou na procura de hora - {}".format(text))
    else:
        print("Falhou na procura de hora - {}".format(text))

    return False


def validate_hour_hh_mm_ss(text):
    regex = re.findall(r'\d{1,2}:\d{2}:\d{2}', text)

    print("REGEX: {}".format(regex))

    if regex:
        hour, minute, second = regex[0].split(":")
        hour = int(hour)
        minute = int(minute)
        second = int(second)

        if hour >= 0 and hour < 24 and minute >= 0 and minute < 60 and second >= 0 and second < 60:
            print("Deu match - {}".format(text))
            return regex[0].strip()
        else:
            print("Falhou na procura de hora - {}".format(text))
    else:
        print("Falhou na procura de hora - {}".format(text))

    return False
