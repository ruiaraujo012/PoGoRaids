#!/usr/bin/python3

import argparse
import math
import cv2 as cv
from matplotlib import pyplot as plt

parser = argparse.ArgumentParser(description='Name of screenshot.')
parser.add_argument('--num', type=int, default=1,
                    help='an integer for the path screen')

args = parser.parse_args()

img = cv.imread('raids/raid_' + str(args.num) + '.jpg')
h, w, c = img.shape

print('Resolution size: {} x {}'.format(h, w))

# Ratio values for cutting image in the same place for every resolution
ratio_top = 0.1197916666
ratio_bottom = 0.3177083333

ratio_left = 0.2129629629
ratio_right = 0.7962962962

# Ratio for get level icon before egg hatch
ratio_egg = 0.90

top = math.ceil(h * ratio_top)
bottom = math.floor(h * ratio_bottom / ratio_egg)
left = math.ceil(w * ratio_left)
right = math.floor(w * ratio_right)

crop_img = img[top:bottom, left:right]

plt.axis("off")
plt.imshow(cv.cvtColor(crop_img, cv.COLOR_BGR2RGB))
plt.show()
