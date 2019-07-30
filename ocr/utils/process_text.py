import re
import pytesseract
from utils import process_img as pri
from utils import name_ratio as nr
from utils import get_bosses as gb


def find_boss_name_from_screenshot(img_name, raid_level):
    # FIXME: remover barra superior, falham as imagens 3, 6 e 41.
    img = pri.read_image_pokemon(img_name)

    new_img = pri.remove_bottom_bar(img)

    processed_img = pri.crop_resize_img(new_img)

    pokemon_name_img = pri.crop_pokemon_name(processed_img)

    thresh = pri.get_threshold(pokemon_name_img, 245, True)

    text_found = pytesseract.image_to_string(
        thresh, config="--psm 8")

    boss_name_found = re.sub('[^a-zA-Z]', '', text_found)

    bosses_id = gb.current_boss_by_level(raid_level)

    bosses = gb.current_boss_names_by_id(bosses_id)

    max_ratio = 0

    for boss_name in bosses:
        ratio = nr.levenshtein_ratio_and_distance(
            boss_name_found.lower(), boss_name.lower(), ratio_calc=True)

        if ratio > max_ratio:
            max_ratio = ratio
            pokemon_name = boss_name

    print('=' * 30)
    print('Text found: {}'.format(text_found))
    print('Text found with regex: {}'.format(boss_name_found))
    print('Best match name: {}'.format(pokemon_name))
    print('Best match ratio: {}'.format(max_ratio))
    print('=' * 30)

    return pokemon_name


def validate_hour_hh_mm(text):
    regex = re.findall(r'\d{1,2}:\d{2}', text)

    if regex:
        hour, minute = regex[0].split(":")
        hour = int(hour)
        minute = int(minute)
        if hour >= 0 and hour < 24 and minute >= 0 and minute < 60:
            return regex[0].strip()

    return False


def validate_hour_hh_mm_ss(text):
    regex = re.findall(r'\d{1,2}:\d{2}:\d{2}', text)

    if regex:
        hour, minute, second = regex[0].split(":")
        hour = int(hour)
        minute = int(minute)
        second = int(second)

        if hour >= 0 and hour < 24 and minute >= 0 and minute < 60 and second >= 0 and second < 60:
            return regex[0].strip()

    return False
