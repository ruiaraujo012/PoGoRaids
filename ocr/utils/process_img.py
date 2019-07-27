import cv2 as cv
import color as co


def read_image(path):
    img_path = "raids/raid_" + str(path) + ".jpg"
    img = cv.imread(img_path)
    return img


def crop_resize_img(img):
    h, w, c = img.shape

    print('Resolution size: {} x {}'.format(h, w))

    width = 900

    crop_img = img[0:int(h/3*2), 0:w]

    img_scale = width/w
    new_x = img.shape[1]*img_scale

    result_img = cv.resize(crop_img, (int(new_x), 960))

    return result_img


def remove_bottom_bar(img):
    h, w, c = img.shape
    print("Prev size {} {}".format(h, w))
    color = img[h-1, 0]

    is_black = co.diff_between_rgb_colors(color[::-1], [0, 0, 0]) < 10
    is_white = co.diff_between_rgb_colors(color[::-1], [255, 255, 255]) < 10
    is_orange = co.diff_between_rgb_colors(color[::-1], [245, 80, 32]) < 10

    cv.imshow("prev image", img)
    cv.waitKey(0)

    print("Color initial {} {}".format(
        color, co.diff_between_rgb_colors(color, img[h-2, 0])))

    if is_black or is_white or is_orange:
        pixel_cut = 0
        while(co.diff_between_rgb_colors(color, img[h-1, 0]) < 5):
            pixel_cut += 1
            h -= 1
            print("{} {}".format(
                h, co.diff_between_rgb_colors(color, img[h, 0])))

        if pixel_cut > 25:
            img = img[0:h, 0:w]
            print("New size {} {}".format(h, w))
            cv.imshow("new image", img)
            cv.waitKey(0)

        h, w, c = img.shape

        print('Resolution size: {} x {}'.format(h, w))

    width = 900
    crop_img = img[0:int(h/3*2), 0:w]


def crop_pokemon_name(img):
    h, w, c = img.shape

    crop_img = img[340:460, int(w * 0.1):int(w * 0.9)]

    return crop_img


def get_threshold(img, thresh_val=240, which=False):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    ret, thresh = cv.threshold(
        gray, thresh_val, 255, cv.THRESH_BINARY_INV)

    kernel = cv.getStructuringElement(cv.MORPH_RECT, (4, 8))
    morph_img = cv.morphologyEx(thresh, cv.MORPH_CLOSE, kernel)

    if which:
        return thresh
    else:
        return morph_img
