#!/usr/bin/python3
import math

# Algorithm for color similarity https://stackoverflow.com/questions/5392061/algorithm-to-check-similarity-of-colors
# RGB to XYZ for both colors
# XYZ to LAB for both colors
# Diff = DeltaE94(LABColor1,LABColor2)


def rgb_to_xyz(color):
    # sR, sG and sB(Standard RGB) input range = 0 ÷ 255
    # X, Y and Z output refer to a D65/2° standard illuminant.

    var_R = (color[0] / 255)
    var_G = (color[1] / 255)
    var_B = (color[2] / 255)

    if (var_R > 0.04045):
        var_R = ((var_R + 0.055) / 1.055) ** 2.4
    else:
        var_R = var_R / 12.92
    if (var_G > 0.04045):
        var_G = ((var_G + 0.055) / 1.055) ** 2.4
    else:
        var_G = var_G / 12.92
    if (var_B > 0.04045):
        var_B = ((var_B + 0.055) / 1.055) ** 2.4
    else:
        var_B = var_B / 12.92

    var_R = var_R * 100
    var_G = var_G * 100
    var_B = var_B * 100

    X = var_R * 0.4124 + var_G * 0.3576 + var_B * 0.1805
    Y = var_R * 0.2126 + var_G * 0.7152 + var_B * 0.0722
    Z = var_R * 0.0193 + var_G * 0.1192 + var_B * 0.9505

    return [X, Y, Z]


def xyz_to_lab(color):
    # Reference-X, Y and Z refer to specific illuminants and observers.
    # Common reference values are available below in this same page.
    # Reference values can be found on the link on top

    reference_X = 94.811
    reference_Y = 100.00
    reference_Z = 107.304

    var_X = color[0] / reference_X
    var_Y = color[1] / reference_Y
    var_Z = color[2] / reference_Z

    if (var_X > 0.008856):
        var_X = var_X ** (1/3)
    else:
        var_X = (7.787 * var_X) + (16 / 116)
    if (var_Y > 0.008856):
        var_Y = var_Y ** (1/3)
    else:
        var_Y = (7.787 * var_Y) + (16 / 116)
    if (var_Z > 0.008856):
        var_Z = var_Z ** (1/3)
    else:
        var_Z = (7.787 * var_Z) + (16 / 116)

    CIE_L = (116 * var_Y) - 16
    CIE_a = 500 * (var_X - var_Y)
    CIE_b = 200 * (var_Y - var_Z)

    return [CIE_L, CIE_a, CIE_b]


def delta_e(color_lab_1, color_lab_2):
    # CIE-L*1, CIE-a*1, CIE-b*1 // Color  # 1 CIE-L*ab values
    # CIE-L*2, CIE-a*2, CIE-b*2 // Color  # 2 CIE-L*ab values

    delta_E = math.sqrt(((color_lab_1[0] - color_lab_2[0]) ** 2)
                        + ((color_lab_1[1] - color_lab_2[1]) ** 2)
                        + ((color_lab_1[2] - color_lab_2[2]) ** 2))

    return delta_E


def similarity(color1, color2):

    XYZ_1 = rgb_to_xyz(color1)
    LAB_1 = xyz_to_lab(XYZ_1)

    XYZ_2 = rgb_to_xyz(color2)
    LAB_2 = xyz_to_lab(XYZ_2)

    delta = delta_e(LAB_1, LAB_2)
    # print("Delta_E {}".format(delta))
    # > 25 não é semelhante
    if delta < 20:
        return True
    return False


def tests():
    c1 = [238, 123, 70]
    c2 = [253, 115, 55]
    c3 = [239, 131, 86]
    c4 = [247, 125, 53]
    c5 = [245, 123, 61]
    c6 = [244, 219, 210]
    c7 = [235, 199, 79]
    c8 = [235, 110, 79]

    print(similarity(c1, c2))
    print(similarity(c1, c3))
    print(similarity(c1, c4))
    print(similarity(c1, c5))
    print("\n\n")
    print(similarity(c2, c3))
    print(similarity(c3, c4))
    print(similarity(c4, c5))
    print(similarity(c1, c6))
    print(similarity(c1, c7))
    print(similarity(c1, c8))
