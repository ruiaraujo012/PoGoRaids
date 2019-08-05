import pytesseract
import cv2 as cv
import numpy as np
from utils import process_img as pi


def scan_for_current_time(img):
    # Verificar 7.8.9 - aparecem a branco
    h, w, c = img.shape
    vscale = h/960
    cropped = img[0:min(int(45*vscale), 65), 0:w]
    gray = cv.cvtColor(cropped, cv.COLOR_BGR2GRAY)
    zoomed = pi.zoom_img(gray, 2, 2)

    # TODO : reajustar estes valores
    thresholds = [190, 200, 210, 165, 150, 130, 100, 85, 50, 25]
    extracted_text = pi.try_multiple_thresholds_ocr(
        zoomed, thresholds, pi.validate_hour_hh_mm)

    return extracted_text


def extract(img):
    h, w, c = img.shape

    phone_time = scan_for_current_time(img)
    raid_time, did_egg_hatch = scan_raid_time(img)

    return phone_time, raid_time, did_egg_hatch


def scan_raid_time(img):
    orange = [243, 121, 53]
    raid_time = pi.section_by_color(img, orange,  [0.86, 0.72], [
                                    0.95, 0.96], 60, 0, [], regex=pi.validate_hour_hh_mm_ss)
    did_egg_hatch = True

    if not raid_time:
        pink = [243, 136, 142]
        raid_time = pi.section_by_color(img, pink,  [0.28, 0.3], [0.485, 0.7], 70, 0, [
        ], pixels_quantity=150, regex=pi.validate_hour_hh_mm_ss)
        did_egg_hatch = False

    return raid_time, did_egg_hatch


def extract_level(img):
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img_gray = cv.GaussianBlur(img_gray, (7, 7), cv.BORDER_DEFAULT)

    template = cv.imread('images/raids/raid_icon.png', 0)
    template = cv.resize(template, None, fx=0.098, fy=0.098,
                         interpolation=cv.INTER_CUBIC)
    template = cv.GaussianBlur(template, (1, 1), cv.BORDER_DEFAULT)

    loc = [[]]
    max_level = 0
    while(True):
        level = 0
        w, h = template.shape[::-1]

        if w < 20 and h < 20:
            break

        # TODO: analizar os elemtnos q se sobrepoem
        res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
        threshold = 0.5
        loc = np.where(res >= threshold)

        for pt in zip(*loc[::-1]):
            cv.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

        # [187, 188, 221, 222, 256, 290, 324, 325])
        x_points = loc[1]
        x_points.sort()

        for (index, point) in enumerate(x_points[:-1]):
            diff = abs(loc[1][index + 1] - point)
            if diff > w/2:
                level += 1

        max_level = max(level, max_level)

        if max_level >= 5:
            max_level = 5
            break

        if len(loc[0]) >= 1 and level == 0:
            level = 1

        template = cv.resize(template, None, fx=0.95,
                             fy=0.95, interpolation=cv.INTER_CUBIC)
        template = cv.GaussianBlur(template, (3, 3), cv.BORDER_DEFAULT)

    return max_level


def extract_gym_name(img, coords):
    w, h, c = img.shape
    img = img[coords[0]-coords[2]:coords[0] +
              coords[2], coords[1]+coords[2]:w]

    img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
    ret, img = cv.threshold(img,
                            205, 255, cv.THRESH_BINARY_INV)

    return pytesseract.image_to_string(
        img, config='--psm 6')
