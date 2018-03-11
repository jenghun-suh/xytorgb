import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cv2
import random

point_x = 0.33
point_y = 0.33
int_value = 1
int_max = 1.2

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

img = np.zeros((270, 480, 3), np.uint8)

#d = {'x': [range(0, 479)], 'y': [range(0, 269)]}
d = {'x': [0, 100, 200], 'y': [0, 100, 200]}
df = pd.DataFrame(data=d)

#for i in range(3):
#    temp_x = df.ix[i, 'x']
#    temp_y = df.ix[i, 'y']
#    print(temp_x, temp_y)
#    cv2.rectangle(img, (temp_x, temp_y), (temp_x + 100, temp_y +100), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), -1)

#for i in range(0, 479):
#    for j in range(0, 269):
#        cv2.rectangle(img, (i, j), (i+1, j+1), ((i+j)*256/750, (i+j)*256/750, (i+j)*256/750), -1)

cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
#cv2.imwrite("test.png", img)
#cv2.imwrite("test.jpg", img)
#cv2.imwrite("test.tif", img)