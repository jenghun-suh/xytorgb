import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point
from shapely.geometry import LineString

import cv2

def convert_xyY_RGB(point_x, point_y, int_value, int_max):

    CIE_y = int_value
    CIE_x = CIE_y * point_x / point_y
    CIE_z = CIE_y * (1 - point_x - point_y) / point_y

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

def convert_xyY_Wd(point_x, point_y, cmf_df):
    # x,y - white line

    point_white = Point(0.33, 0.33)
    point_xy = Point(point_x, point_y)

    point_x_list = [point_xy.x, point_white.x]
    point_y_list = [point_xy.y, point_white.y]

    extpol_coeff = np.polyfit(point_x_list, point_y_list, 1)
    extpol_eq = np.poly1d(extpol_coeff)
    extpol_x = np.linspace(0, 0.8, 100)
    extpol_y = extpol_eq(extpol_x)

    # CMF line

    cmf_x = cmf_df['x']
    cmf_y = cmf_df['y']

    # Intersection

    cmf_line = LineString(list(zip(cmf_x, cmf_y)))
    extpol_line = LineString(list(zip(extpol_x, extpol_y)))

    # Point selection

    temp_points = cmf_line.intersection(extpol_line)
    points_xmin, points_ymin, points_xmax, points_ymax = temp_points.bounds

    if (points_xmin == points_xmax) & (points_ymin == points_ymax):
        point_intersec = temp_points
        distance_intersec = temp_points.distance(point_white)

    else:
        temp_point_1, temp_point_2 = cmf_line.intersection(extpol_line)

        if point_x > point_white.x:
            if temp_point_1.x > temp_point_2.x:
                point_intersec = temp_point_1
            elif temp_point_2.x > temp_point_1.x:
                point_intersec = temp_point_2
        elif point_x < point_white.x:
            if temp_point_1.x < temp_point_2.x:
                point_intersec = temp_point_1
            elif temp_point_2.x < temp_point_1.x:
                point_intersec = temp_point_2

    distance_intersec = point_intersec.distance(point_white)

    # Purity Calculation

    distance_points = point_xy.distance(point_white)
    Purity_value = distance_points / distance_intersec * 100

    # Wd Calculation

    cmf_xy = list(zip(cmf_x, cmf_y))

    Table_Distance = []
    i = 360

    for temp_cmf_point in cmf_xy:
        temp_Point = Point(temp_cmf_point)
        temp_distance = point_intersec.distance(temp_Point)
        i += 1
        Table_Distance.append(temp_distance)

    cmf_Temp = cmf_df
    cmf_Temp['Distance'] = pd.Series(Table_Distance, index=cmf_df.index)
    cmf_Temp = cmf_Temp.sort_values(by=['Distance'])
    cmf_Temp_1 = cmf_Temp.iloc[0]
    cmf_Temp_2 = cmf_Temp.iloc[1]

    if cmf_Temp_1['Wavelength(nm)'] < cmf_Temp_2['Wavelength(nm)']:
        Wd_value = cmf_Temp_1['Wavelength(nm)'] + (cmf_Temp_1['Distance']) / (
                    cmf_Temp_1['Distance'] + cmf_Temp_2['Distance'])

    elif cmf_Temp_1['Wavelength(nm)'] > cmf_Temp_2['Wavelength(nm)']:
        Wd_value = cmf_Temp_1['Wavelength(nm)'] - (cmf_Temp_1['Distance']) / (
                    cmf_Temp_1['Distance'] + cmf_Temp_2['Distance'])

    else:
        Wd_value = cmf_Temp_1['Wavelength(nm)']

    return Wd_value, Purity_value


"""
To do list

1. Red/Green/Blue RGB func.
2. Input data + Merged RGB/purity/Wd writing

"""

cmf_df = pd.read_csv('CIE 1931 XYZ.csv')
df = pd.read_csv('test.txt', sep = '\t')

img = np.zeros((300, 300, 3), np.uint8)
int_max = 256

for idx, row in df.iterrows():
    temp_x = int(row['x'])
    temp_y = int(row['y'])
    temp_Red_int = row['Red_int']
    temp_Red_x = row['Red_x']
    temp_Red_y = row['Red_y']
    temp_R, temp_G, temp_B = convert_xyY_RGB(temp_Red_x, temp_Red_y, temp_Red_int, int_max)
    cv2.rectangle(img, (temp_x * 100, temp_y * 100), ((temp_x + 1) * 100, (temp_y + 1) * 100), (temp_B, temp_G, temp_R), -1)
    print(convert_xyY_Wd(temp_Red_x, temp_Red_y, cmf_df))

cv2.imwrite("test.png", img)
cv2.imwrite("test.jpg", img)
cv2.imwrite("test.tif", img)
cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
