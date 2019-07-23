import re
import numpy as np
import color
import pytesseract
import text_validation
import cv2 as cv

# Color [ R, G, B]
# Start [yScale, xScale]
# End [yScale, xScale]


def section_by_color(img, color_goal, start, end, block_height, threshold_type, thresholds, pixels_quantity=85, regex=()):
    color_found_initial_coords = []
    found_pixels = []
    count_pixels = 0
    h, w, c = img.shape

    vscale = h/960
    hscale = w/500

    print("Block heigh {}".format(block_height))

    # y,x
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
        if color.arbitrary_similarity(img[y, x][::-1], color_goal, 20):
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
                # thresholds = [180, 190, 200, 210, 215, 100, 125, 150, 175]
                text = try_multiple_thresholds_ocr(zoomed, thresholds, regex)

            if text:
                print("[img_proc] Text extracted {}".format(text))
                return text

            break


def cut_block(img, found_pixels, block_height):
    min_x = 9999
    max_x = -1
    section_max_height = 9999

    for arr in found_pixels:
        if arr[1] < min_x:
            min_x = arr[1]
            color_found_initial_coords = arr
        if arr[1] > max_x:
            max_x = arr[1]

    box_width = max_x - min_x
    sec_x = color_found_initial_coords[1]
    sec_y = color_found_initial_coords[0]

    # print("Encontrou um bloco de cor com inicio em x.{} y.{}".format(
    #     sec_x, sec_y))

    return img[sec_y:sec_y+block_height, sec_x:sec_x+box_width]


def zoom_img(img, fx, fy):
    return cv.resize(img, None, fx=2, fy=2,
                     interpolation=cv.INTER_CUBIC)


def threshold_binary_inv(gray_img, thresh_val, regex=()):
    ret, thresh = cv.threshold(
        gray_img, thresh_val, 255, cv.THRESH_BINARY_INV)

    cv.imshow("img", thresh)
    cv.waitKey(0)
    cv.destroyAllWindows()

    text = ocr_numbers_single_row(thresh)
    extracted_text = regex(text)

    if extracted_text:
        return extracted_text

    return None


def try_multiple_thresholds_pokemon_name(gray_img, thresholds):

    for th in thresholds:
        print("Testing for thr {}".format(th))
        ret, thresh = cv.threshold(gray_img, th, 255, cv.THRESH_BINARY_INV)

        kernel = np.ones((5, 4), np.uint8)
        img_erode = cv.erode(thresh, kernel, iterations=1)

        cv.imshow("img", img_erode)
        cv.waitKey(0)
        cv.destroyAllWindows()

        text = pytesseract.image_to_string(
            thresh)  # config='--psm 12'

        print("Pokemon name {}".format(text))

    return None


def try_multiple_thresholds_ocr(gray_img, thresholds, regex=()):

    for th in thresholds:
        # print("Testing for thr {}".format(th))
        ret, thresh = cv.threshold(gray_img, th, 255, cv.THRESH_BINARY_INV)
        cv.imshow("img", thresh)
        cv.waitKey(0)
        cv.destroyAllWindows()

        text = ocr_numbers_single_row(thresh)

        if not regex == ():
            extracted_text = regex(text)

        if extracted_text:
            return extracted_text

    return None


def ocr_numbers_single_row(img):
    return pytesseract.image_to_string(
        img, config='-c tessedit_char_whitelist=1234567890:~-AMP --psm 7')


def remove_noise(img):
    filtered = cv.adaptiveThreshold(img.astype(
        np.uint8), 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 9, 41)
    kernel = np.ones((1, 1), np.uint8)
    opening = cv.morphologyEx(filtered, cv.MORPH_OPEN, kernel)
    closing = cv.morphologyEx(opening, cv.MORPH_CLOSE, kernel)
    or_image = cv.bitwise_or(img, closing)
    return or_image
