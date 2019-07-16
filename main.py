#!/usr/bin/python3

import pytesseract
import sys
import cv2

from PIL import Image

# TODO : adapt coordinates to scales


def crop_image(img, coords):
    cropped = img.crop(coords)
    cropped.show()
    text = pytesseract.image_to_string(cropped)
    print(text)


im = Image.open(sys.argv[1])
text = pytesseract.image_to_string(im)

print("Raw OCR")
print(text)

# Crop time until raid start
print("Time until start:")
coords = (315, 445, 385, 470)
cropped_img = crop_image(im, coords)

# Crop CP
#coords = (84, 117, 353, 185)
#cropped_img = crop_image(im, coords)
