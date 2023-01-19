import numpy as np
from scipy import ndimage, misc
from skimage import io, data, filters, measure, morphology, img_as_ubyte
import plotly.express as px
from skimage.morphology import * 
from skimage.filters import unsharp_mask
from skimage.color import rgb2gray
import cv2

img = io.imread('Images/FarmPlots.jpg')
grey = rgb2gray(img)
Sharp = unsharp_mask(grey, radius=50)
median = ndimage.median_filter(Sharp, size=4)
sobel = filters.sobel(median)

threshold = filters.threshold_otsu(sobel)
arr = sobel > threshold
FirstClean = morphology.remove_small_objects(arr, 35)
SecondClean = morphology.remove_small_holes(FirstClean, 35)

Dselem = disk(3)
Cselem = disk(8)
dilated = morphology.dilation(SecondClean, Dselem)
closed = morphology.closing(dilated, Cselem)

new = np.array(closed, dtype= np.uint8)
contours, _= cv2.findContours(new, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

for idx, contour in enumerate(contours) :
    approx = cv2.approxPolyDP(contour, 0.001 * cv2.arcLength(contour, True), True)       
    cv2.drawContours(img, [approx], -1, (0, 0, 255), 3) 
    n = approx.ravel() 
    area = cv2.contourArea(contour) 
    perimeter = cv2.arcLength(contour,True)
        

    CoordX = int(sum(contour[:,0,0]) / len(contour))
    CoordY = int(sum(contour[:,0,1]) / len(contour))
    cv2.putText(img, str(idx), (CoordX, CoordY), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    #cv2.putText(img, str(area), (CoordX, CoordY - 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    #cv2.putText(img, str(perimeter), (CoordX, CoordY - 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)