#!/usr/bin/python3


import re
import pytesseract
import cv2 as cv
from utils import process_img as pri
from utils import name_ratio as nr

TOTAL_RAIDS = 54

for i in range(0, TOTAL_RAIDS):
    # FIXME: remover barra superior, falham as imagens 3, 6 e 41.

    img = pri.read_image_pokemon(i)

    new_img = pri.remove_bottom_bar(img)

    processed_img = pri.crop_resize_img(new_img)

    h, w, c = processed_img.shape

    pokemon_name_img = pri.crop_pokemon_name(processed_img)

    thresh = pri.get_threshold(pokemon_name_img, 245, True)

    text = pytesseract.image_to_string(
        thresh, config="--psm 8")

    text = re.sub('[^a-zA-Z]', '', text).lower()

    names = ['raikou', 'mesprit', 'dialga',
             'giratina', 'rayquaza', 'raichu', 'scyther', 'togetic', 'mewtwo', 'articuno', 'drifloon',
             'machamp', 'sneasel', 'tyranitar', 'graudon', 'cresselia', 'metagross', 'dragonite',
             'latios', 'marowak', 'hitmonlee', 'absol', 'latias']

    max_ratio = 0
    pokemon_name = 'not found'

    for name in names:
        distance = nr.levenshtein_ratio_and_distance(text, name)
        ratio = nr.levenshtein_ratio_and_distance(text, name, ratio_calc=True)

        if ratio > max_ratio:
            max_ratio = ratio
            pokemon_name = name

    print(' ' * 20)
    print('=' * 20)
    print('Text found: {}'.format(text))
    print('Best match name: {}'.format(pokemon_name))
    print('Best match ratio: {}'.format(max_ratio))
    print('=' * 20)

    cv.imshow("raid_" + str(i) + ".jpg", thresh)
    cv.waitKey(0)
    cv.destroyAllWindows()
