import cv2
import numpy as np
import glob
import time
input = 'MIAS6'
i = 0
start = time.time()
for img in glob.glob(input + '/1/*.png'):
    image = cv2.imread(img,0)
    kernel = np.ones((120,120),np.uint8)
    erosion = cv2.erode(image,kernel,iterations = 1)
    kernel = np.ones((120,120),np.uint8)
    dilation = cv2.dilate(erosion, kernel, iterations = 1)
    merged = cv2.bitwise_and(image, image , mask=dilation)
    i += 1
end = time.time()
print(end-start)