import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cv2
import random

def convert_xyY_RGB(point_x, point_y, int_value, int_max):
    CIE_y = int_value
    CIE_x = CIE_y * point_x / point_y
    CIE_z = CIE_y * (1 - point_x - point_y) / point_y

    M = ([1.9634, -0.6105, -0.3413], [-0.9787, 1.9161, 0.3345], [0.0286, -0.01406, 1.3487])

    RGB_r =   2.0413 * CIE_x - 0.5649 * CIE_y - 0.3447 * CIE_z
    RGB_g = - 0.9692 * CIE_x + 1.8760 * CIE_y + 0.0415 * CIE_z
    RGB_b =   0.0134 * CIE_x - 0.1183 * CIE_y + 1.0153 * CIE_z

    scale_value = int_value * 255 / int_max

    RGB_r *= scale_value
    RGB_g *= scale_value
    RGB_b *= scale_value

    RGB_r = int(RGB_r)
    RGB_g = int(RGB_g)
    RGB_b = int(RGB_b)

    return RGB_r, RGB_g, RGB_b


df = pd.read_csv('test.txt', sep = '\t')
img = np.zeros((300, 300, 3), np.uint8)
int_max = 256
print(df)

for i in range(9):
    temp_x = df.ix[i, 'x']
    temp_y = df.ix[i, 'y']
    temp_Red_int = df.ix[i, 'Red_int']
    temp_Red_x = df.ix[i, 'Red_x']
    temp_Red_y = df.ix[i, 'Red_y']
    temp_R, temp_G, temp_B = convert_xyY_RGB(temp_Red_x, temp_Red_y, temp_Red_int, int_max)
    cv2.rectangle(img, (temp_x * 100, temp_y * 100), ((temp_x + 1) * 100, (temp_y + 1) * 100), (temp_B, temp_G, temp_R), -1)
    print(temp_R, temp_G, temp_B)

cv2.imwrite("test.png", img)
cv2.imwrite("test.jpg", img)
cv2.imwrite("test.tif", img)

cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
