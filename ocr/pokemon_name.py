#!/usr/bin/python3


import re
import pytesseract
import cv2 as cv
from utils import process_img as pri
from utils import name_ratio as nr
from utils import get_bosses as gb


TOTAL_RAIDS = 54

for i in range(0, TOTAL_RAIDS):
    # FIXME: remover barra superior, falham as imagens 3, 6 e 41.

    img = pri.read_image_pokemon(i)

    new_img = pri.remove_bottom_bar(img)

    processed_img = pri.crop_resize_img(new_img)

    h, w, c = processed_img.shape

    pokemon_name_img = pri.crop_pokemon_name(processed_img)

    thresh = pri.get_threshold(pokemon_name_img, 245, True)

    text_found = pytesseract.image_to_string(
        thresh, config="--psm 8")

    boss_name_found = re.sub('[^a-zA-Z]', '', text_found)

    # TODO: Adicionar um metodo que devolva o nivel da raid e alterar em baixo (default 5)
    # Sem alterar todos vão ser Mewtwo, Dialga e Raikou
    bosses_id = gb.current_boss_by_level(5)

    bosses = gb.current_boss_names_by_id(bosses_id)

    max_ratio = 0

    for boss_name in bosses:
        distance = nr.levenshtein_ratio_and_distance(
            boss_name_found.lower(), boss_name.lower())
        ratio = nr.levenshtein_ratio_and_distance(
            boss_name_found.lower(), boss_name.lower(), ratio_calc=True)

        if ratio > max_ratio:
            max_ratio = ratio
            pokemon_name = boss_name

    print(' ' * 20)
    print('=' * 20)
    print('Text found: {}'.format(text_found))
    print('Text found with regex: {}'.format(boss_name_found))
    print('Best match name: {}'.format(pokemon_name))
    print('Best match ratio: {}'.format(max_ratio))
    print('=' * 20)

    cv.imshow("raid_" + str(i) + ".jpg", thresh)
    cv.waitKey(0)
    cv.destroyAllWindows()
