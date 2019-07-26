#!/usr/bin/python3


import re
import pytesseract
import cv2 as cv
from utils import process_img as pri

TOTAL_RAIDS = 54

for i in range(0, TOTAL_RAIDS):

    # FIXME: remover barra superior, falham as imagens 6 e 41.

    img_path = pri.read_image_pokemon(i)

    img = cv.imread(img_path)

    new_img = pri.remove_bottom_bar(img)

    processed_img = pri.crop_resize_img(new_img)

    h, w, c = processed_img.shape

    pokemon_name_img = pri.crop_pokemon_name(processed_img)

    thresh = pri.get_threshold(pokemon_name_img, 245, True)

    text = pytesseract.image_to_string(
        thresh, config="--psm 8")

    text = re.sub('[^a-zA-Z]', '', text).lower()

    print('Text found: {}'.format(text))

    cv.imshow("raids/raid_" + str(i) + ".jpg", thresh)
    cv.waitKey(0)
    cv.destroyAllWindows()
