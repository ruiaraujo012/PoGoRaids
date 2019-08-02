import pytesseract
import cv2 as cv
import numpy as np
from utils import process_img as pi
from utils import process_text as pt


def scan_for_current_time(img):
    # Verificar 7.8.9 - aparecem a branco
    h, w, c = img.shape
    vscale = h/960
    cropped = img[0:min(int(45*vscale), 65), 0:w]
    gray = cv.cvtColor(cropped, cv.COLOR_BGR2GRAY)
    zoomed = pi.zoom_img(gray, 2, 2)

    ret, thresh = cv.threshold(zoomed, 50, 255, cv.THRESH_BINARY_INV)

    # TODO : reajustar estes valores
    thresholds = [190, 200, 210, 165, 150, 130, 100, 85, 50, 25]
    extracted_text = pi.try_multiple_thresholds_ocr(
        zoomed, thresholds, pt.validate_hour_hh_mm)

    return extracted_text


def extract(img):
    h, w, c = img.shape

    phone_time = scan_for_current_time(img)
    time_until_finish, did_egg_hatch = scan_for_time_until_finish(img)

    return phone_time, time_until_finish, did_egg_hatch


def scan_for_time_until_finish(img):
    orange = [243, 121, 53]
    time_until_finish = pi.section_by_color(img, orange,  [0.5, 0.65], [0.8, 0.99], 34, 0, [
    ], regex=pt.validate_hour_hh_mm_ss)
    did_egg_hatch = True

    if not time_until_finish:
        # print("Testing timer before hatch")
        pink = [243, 136, 142]
        time_until_finish = pi.section_by_color(img, pink,  [0.15, 0.2], [0.45, 0.85], 50, 0, [
        ], pixels_quantity=150, regex=pt.validate_hour_hh_mm_ss)
        did_egg_hatch = False

    return time_until_finish, did_egg_hatch


def extract_level(img):
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img_gray = cv.GaussianBlur(img_gray, (9, 9), cv.BORDER_DEFAULT)

    template = cv.imread('images/raids/raid_icon.png', 0)
    template = cv.resize(template, None, fx=0.098, fy=0.098,
                         interpolation=cv.INTER_CUBIC)
    # template = cv.GaussianBlur(template, (9, 9), cv.BORDER_DEFAULT)

    print(template.shape)
    print(img_gray.shape)

    cv.imshow('res.png', img_gray)
    cv.imshow('res2.png', template)
    cv.waitKey(0)

    loc = [[]]
    max_level = 0
    while(True):
        level = 0
        w, h = template.shape[::-1]

        if w < 20 and h < 20:
            break

        # print(w, h)
        # TODO: analizar os elemtnos q se sobrepoem

        res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
        threshold = 0.5
        loc = np.where(res >= threshold)
        # print(loc)

        for pt in zip(*loc[::-1]):
            cv.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

            # cv.imshow('res2.png', img)
            # cv.waitKey(0)

        # [187, 188, 221, 222, 256, 290, 324, 325])

        x_points = loc[1]
        x_points.sort()

        # print("XPOINTS")
        # print(x_points)

        for (index, point) in enumerate(x_points[:-1]):
            # print(index)
            # print(point)
            diff = abs(loc[1][index + 1] - point)
            # print(diff)
            # print('w: {}'.format(w/2))
            if diff > w/2:
                # print("Prev {} - Next {}".format(point, loc[1][index+1]))
                level += 1

        max_level = max(level, max_level)

        if max_level >= 5:
            max_level = 5
            break

        if len(loc[0]) >= 1 and level == 0:
            level = 1
            # cv.imshow("output", img_rgb)
            # cv.imshow("output2", template)
            # cv.waitKey(0)

        template = cv.resize(template, None, fx=0.95,
                             fy=0.95, interpolation=cv.INTER_CUBIC)

    # print("Level {}".format(max_level))

    print('m: {}'.format(max_level))

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
