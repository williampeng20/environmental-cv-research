import cv2
import numpy as np
from util import *

img = cv2.imread('IMG_4465_zoom.jpg')

import os
cwd = os.getcwd()
#Canny Edge Detection
binary_img = cv2.Canny(img, 100, 110)
cv2.imwrite(cwd+'/canny_edge/IMG_4468_zoom_canny_edge.jpg', binary_img)


#ret,thresh = cv2.threshold(binary_img,127,255,0)
#_, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
_, contours, hierarchy = cv2.findContours(binary_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

#RETR_TREE : retrieves all of the contours and reconstructs a full hierarchy of nested contours.
#CHAIN_APPROX_SIMPLE : compresses horizontal, vertical, and diagonal segments and leaves only their end points.
    #For example, an up-right rectangular contour is encoded with 4 points.

print "Original # of Contours:",len(contours) #how many contour lines
#print contours
prunedContours = [contour for contour in contours if len(contour) > 4]
print "Filtering contours for at least 4 points:",len(prunedContours)

#area stats
#area = [cv2.contourArea(contour) for contour in prunedContours if cv2.contourArea(contour) > 0]
height, width = img.shape[:2]
img_covered = np.zeros((height, width))
prunedContours.sort(reverse=True, key=lambda x: xy_area(x))
area = [xy_area(contour) for contour in prunedContours if not over_lapping(contour, img_covered)]
area_np = np.array(area)
area_np = reject_outliers(area_np)
print "Min area:", min(area_np)
print "Max area:", max(area_np)
mean = np.mean(area_np)
print "Mean area:",mean
print "Median area:",np.median(area_np)
std = np.std(area_np)
print "STD:",std
#Buckets
print "10% Bucket:",len([a for a in area_np if a < max(area_np)*0.1])
print "20% Bucket:",len([a for a in area_np if a >= max(area_np)*0.1  and a < max(area_np)*0.2])
print "30% Bucket:",len([a for a in area_np if a >= max(area_np)*0.2  and a < max(area_np)*0.3])
print "40% Bucket:",len([a for a in area_np if a >= max(area_np)*0.3  and a < max(area_np)*0.4])
print "50% Bucket:",len([a for a in area_np if a >= max(area_np)*0.4  and a < max(area_np)*0.5])
print "60% Bucket:",len([a for a in area_np if a >= max(area_np)*0.5  and a < max(area_np)*0.6])
print "70% Bucket:",len([a for a in area_np if a >= max(area_np)*0.6  and a < max(area_np)*0.7])
print "80% Bucket:",len([a for a in area_np if a >= max(area_np)*0.7  and a < max(area_np)*0.8])
print "90% Bucket:",len([a for a in area_np if a >= max(area_np)*0.8  and a < max(area_np)*0.9])
print "100% Bucket:",len([a for a in area_np if a >= max(area_np)*0.9])

#prune for only in the center 2 std
img_covered = np.zeros((height, width))
prunedContours = [contour for contour in prunedContours if xy_area(contour) > mean-std and not over_lapping(contour, img_covered)]
print "Final # of contours:", len(prunedContours)

cv2.drawContours(img, prunedContours, -1, (0,255,0), 1)

cv2.imwrite(cwd+'/contour_overlay/IMG_4465_zoom_contour.jpg', img)
