import re
import datetime as dt
import pytesseract
import cv2 as cv
import numpy as np
from utils import color as co
from utils import get_bosses as gb
from utils import extractor as ex
from packages import name_ratio as nr
from fuzzywuzzy import fuzz


def read_image(img_name):
    img_path = "images/raids/" + str(img_name)
    img = cv.imread(img_path)
    return img


def crop_resize_img(img):
    h, w, c = img.shape

    width = 900

    crop_img = img[0:int(h/3*2), 0:w]

    img_scale = width/w
    new_x = img.shape[1]*img_scale

    result_img = cv.resize(crop_img, (int(new_x), 960))

    return result_img


def crop_pokemon_name(img):
    h, w, c = img.shape

    crop_img = img[355:475, int(w * 0.1):int(w * 0.9)]

    return crop_img


def crop_raid_level(img, raid_hatched):
    h, w, c = img.shape

    if raid_hatched:
        crop_img = img[int(h * 0.21):int(h * 0.27),
                       int(w * 0.3):int(w * 0.7)]
        crop_img = cv.resize(crop_img, None, fx=1.4, fy=1.4,
                             interpolation=cv.INTER_CUBIC)
    else:
        crop_img = img[int(h * 0.4):int(h * 0.55),
                       int(w * 0.25):int(w * 0.75)]

    return crop_img


def get_threshold(img, thresh_val=240, which=False):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    gray = cv.GaussianBlur(gray, (3, 3), cv.BORDER_DEFAULT)

    ret, thresh = cv.threshold(
        gray, thresh_val, 255, cv.THRESH_BINARY_INV)

    if which:
        return thresh
    else:
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (4, 8))
        morph_img = cv.morphologyEx(thresh, cv.MORPH_CLOSE, kernel)
        return morph_img


def remove_bottom_bar(img):
    h, w, c = img.shape

    color = img[h-1, 0]

    is_black = co.diff_between_rgb_colors(color[::-1], [0, 0, 0]) < 10
    is_white = co.diff_between_rgb_colors(color[::-1], [255, 255, 255]) < 10
    is_orange = co.diff_between_rgb_colors(color[::-1], [245, 80, 32]) < 10

    if is_black or is_white or is_orange:
        pixel_cut = 0
        while(co.diff_between_rgb_colors(color, img[h-1, 0]) < 5):
            pixel_cut += 1
            h -= 1

        if pixel_cut > 25:
            img = img[0:h, 0:w]

    return img


def zoom_img(img, fx, fy):
    return cv.resize(img, None, fx=2, fy=2,
                     interpolation=cv.INTER_CUBIC)


def try_multiple_thresholds_ocr(gray_img, thresholds, regex=()):

    for th in thresholds:
        ret, thresh = cv.threshold(gray_img, th, 255, cv.THRESH_BINARY_INV)

        text = ocr_numbers_single_row(thresh)

        if not regex == ():
            extracted_text = regex(text)

        if extracted_text:
            return extracted_text

    return None


def ocr_numbers_single_row(img):
    return pytesseract.image_to_string(
        img, config='-c tessedit_char_whitelist=1234567890:~-AMP --psm 7')


def section_by_color(img, color_goal, start, end, block_height, threshold_type, thresholds, pixels_quantity=85, regex=()):
    found_pixels = []
    count_pixels = 0
    h, w, c = img.shape

    vscale = h/960
    hscale = w/500

    init_x = int(w * start[1])
    init_y = int(h * start[0])

    x = init_x
    y = init_y

    max_x = int(w*end[1])
    max_y = int(h*end[0])

    while(True):

        # Nothing relevant extracted
        if x > max_x and y > max_y:
            return None

        if x < max_x:
            x += 1
        else:
            x = init_x
            if y > max_y:
                break
            y += 1

        # WARNING img[y,x] returns BGR instead of RGB
        if co.arbitrary_similarity(img[y, x][::-1], color_goal, 20):
            count_pixels += 1
            found_pixels.append([y, x])
        else:
            count_pixels = 0

        if count_pixels > int(pixels_quantity * hscale):
            cut_img = cut_block(img, found_pixels, int(block_height * vscale))
            gray = cv.cvtColor(cut_img, cv.COLOR_BGR2GRAY)
            zoomed = zoom_img(gray, 2, 2)
            text = ''

            if threshold_type == 0:
                text = threshold_binary_inv(zoomed, 200, regex)
            elif threshold_type == 1:
                text = try_multiple_thresholds_ocr(zoomed, thresholds, regex)

            if text:
                return text

            break


def cut_block(img, found_pixels, block_height):
    min_x = 9999
    max_x = -1

    for arr in found_pixels:
        if arr[1] < min_x:
            min_x = arr[1]
            color_found_initial_coords = arr
        if arr[1] > max_x:
            max_x = arr[1]

    box_width = max_x - min_x
    sec_x = color_found_initial_coords[1]
    sec_y = color_found_initial_coords[0]

    return img[sec_y:sec_y+block_height, sec_x:sec_x+box_width]


def threshold_binary_inv(gray_img, thresh_val, regex=()):
    ret, thresh = cv.threshold(
        gray_img, thresh_val, 255, cv.THRESH_BINARY_INV)

    text = ocr_numbers_single_row(thresh)
    extracted_text = regex(text)

    if extracted_text:
        return extracted_text

    return None


def detect_circles(img):

    output = img.copy()
    gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

    # detect circles in the image
    circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT,
                              2, 150,  minRadius=25, maxRadius=100)

    image_circle = None
    # ensure at least some circles were found
    if circles is not None:
        # convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")

        min_x = 9999
        min_y = 9999
        # loop over the (x, y) coordinates and radius of the circles
        for (x, y, r) in circles:
            if x < min_x and y < min_y:
                min_x = x
                min_y = y
                image_circle = (min_y, min_x, r)

    return image_circle


def find_boss_name(img, raid_level):
    # FIXME: remover barra superior, falham as imagens
    pokemon_name_img = crop_pokemon_name(img)

    thresh = get_threshold(pokemon_name_img, 245, True)

    text_found = pytesseract.image_to_string(
        thresh, config="--psm 8")

    boss_name_found = re.sub('[^a-zA-Z]', '', text_found)

    bosses_id = gb.current_boss_by_level(raid_level)

    bosses = gb.current_boss_names_by_id(bosses_id)

    max_ratio = 0

    for boss_name in bosses:
        ratio = fuzz.ratio(boss_name_found.lower(), boss_name.lower())

        if ratio > max_ratio:
            max_ratio = ratio
            pokemon_name = boss_name

    if max_ratio != 0:
        print('=' * 30)
        print('Text found: {}'.format(text_found))
        print('Text found with regex: {}'.format(boss_name_found))
        print('Best match name: {}'.format(pokemon_name))
        print('Best match ratio: {}'.format(max_ratio))
        print('=' * 30)
    else:
        pokemon_name = None

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


def get_time(phone_time, raid_time):
    if phone_time and raid_time:
        phone_time = dt.datetime.strptime(phone_time, '%H:%M')

        raid_time = dt.datetime.strptime(raid_time, '%H:%M:%S')

        delta = dt.timedelta(hours=raid_time.hour, minutes=raid_time.minute,
                             seconds=raid_time.second)

        time = (phone_time + delta).time().strftime("%H:%M:%S")
    else:
        time = None

    return time


def process_img(img, portals):

    img_no_bottom = remove_bottom_bar(img)
    croped_img = crop_resize_img(img_no_bottom)

    phone_time, raid_time, did_egg_hatch = ex.extract(croped_img)

    level_img = crop_raid_level(
        croped_img, did_egg_hatch)
    raid_level = ex.extract_level(level_img)

    if raid_level == 0:
        print(' Error! '.center(40, '*'))
        print(" Can't read raid level! ".center(40, '*'))
        print(''.center(40, '*'))

    coords = detect_circles(img)

    pokemon_name = None

    if coords:
        gym_name = ex.extract_gym_name(img, coords)

        if portals:
            max_ratio = 0

            for portal in portals:
                ratio = fuzz.ratio(portal['name'].lower(), gym_name.lower())

                if ratio > max_ratio:
                    max_ratio = ratio
                    best_match = portal['name']

            if max_ratio >= 0.8:
                gym_name = best_match
            else:
                print('Best gym name match: {}'.format(best_match))

    if did_egg_hatch:
        pokemon_name = find_boss_name(croped_img, raid_level)

        if pokemon_name == None:
            print(' Error! '.center(40, '*'))
            print(" Can't read pokemon name! ".center(40, '*'))
            print(''.center(40, '*'))

    raid_hour = get_time(phone_time, raid_time)

    return phone_time, raid_time, did_egg_hatch, gym_name, raid_level, pokemon_name, raid_hour
