import cv2 as cv
import color as co


def read_image_pokemon(number):
    img_path = "raids/pokemon/" + str(number) + ".jpg"
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
