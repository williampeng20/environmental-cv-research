import cv2
import numpy as np
from util import *
import os
import sys
import random

assert len(sys.argv) == 5, "Need image name, and # of iter, dist_thresh, area_thresh"
img_name = sys.argv[1][:len(sys.argv[1])-4]
img = cv2.imread(sys.argv[1])

cwd = os.getcwd()
#Canny Edge Detection
binary_img = cv2.Canny(img, 100, 110)
cv2.imwrite(cwd+'/canny_edge/'+img_name+'_canny_edge.jpg', binary_img)

#should correspond to average amount of fragmentation
iterations = int(sys.argv[2])
px_mm = 1818/float(140)
#In the form (px / mm)
# TODO This needs to be dynamic to image

#ret,thresh = cv2.threshold(binary_img,127,255,0)
#_, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
_, contours, hierarchy = cv2.findContours(binary_img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

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
#------------------------------------------------------------------
print "------Initial Stats------"
median_area = stats(prunedContours, xy_area, 0, 999999)
#---------------------------------------------------------------------
"""print "------Throwing out areas with 10 times the median----------"
prunedContours = [contour for contour in prunedContours if xy_area(contour) < 10*median_area]
median_area = stats(prunedContours, xy_area, 0, 10*median_area)"""
#-------------------------------------------------------------------------
print "------polyContoursDP------"
polyContours = [cv2.approxPolyDP(contour, 3, True) for contour in prunedContours]
poly_median_area = stats(polyContours, cv2.contourArea, 0, 999999)
polyContours.sort(reverse=True, key=lambda x: cv2.contourArea(x))
print "Final # of polyContours:", len(polyContours)
#-------------------------------------------------------------------------
print "---------merging contours-----------"
polyContours = [contour for contour in polyContours if len(contour) > 5]
print "# of polyContours (len > 5): ", len(polyContours)
polyContours.sort(reverse=False, key=lambda x: cv2.contourArea(x))
"""mergedContours = []
alreadyMerged = {}
for i in range(0, len(polyContours)):
    alreadyMerged[i] = []
for i in range(0, len(polyContours)):
    contour1 = polyContours[i]
    for j in range(0, len(polyContours)):
        contour2 = polyContours[j]
        if i != j and (distance(contour1[0], contour2[0]) < 6 or distance(contour1[len(contour1)-1], contour2[0]) < 6
         or distance(contour1[0], contour2[len(contour2)-1]) < 6 or distance(contour1[len(contour1)-1], contour2[len(contour2)-1]) < 6):
            if j not in alreadyMerged[i]:
                mergedContours += [np.concatenate((contour1, contour2))]
                alreadyMerged[i] += [j]
                alreadyMerged[j] += [i]
    if len(alreadyMerged[i]) == 0:
        mergedContours += [contour1]"""
a_thresh = float(sys.argv[4])
d_thresh = float(sys.argv[3])
mergedContours = merging(polyContours, area_thresh=a_thresh, dist_thresh=d_thresh, px_mm=px_mm)
for i in range(iterations):
    print "Iteration ", i, len(mergedContours)
    mergedContours.sort(reverse=False, key=lambda x: cv2.contourArea(x))
    mergedContours = merging(mergedContours, area_thresh=a_thresh, dist_thresh=d_thresh, px_mm=px_mm)
print "# of mergedContours:", len(mergedContours)
#close contours
merge_median_area = stats(mergedContours, cv2.contourArea, 0, 999999)
print [cv2.contourArea(contour) for contour in mergedContours]
print "Final # of mergedContours:", len(mergedContours)
#-------------------------------------------------------------------------
print "---------final-----------"
#print cv2.minAreaRect(mergedContours[40])
for i in range(0, len(mergedContours)):
    tmp_img = cv2.imread(sys.argv[1])
    cv2.drawContours(tmp_img, mergedContours, i, (0,255,0), 1)
    cv2.imwrite(cwd+'/contour_overlay/'+str(i)+'_contour.jpg', tmp_img)

#area_thresh=200, dist_thresh=50, use xy_area for merging area diff
"""x = 11
y = 28
print "center dist",x, y, distance(centroid(mergedContours[x]), centroid(mergedContours[y]))
contour1_ellipse = cv2.fitEllipse(mergedContours[x])
contour2_ellipse = cv2.fitEllipse(mergedContours[y])
print "cross_dist", max(5*px_mm, contour1_ellipse[1][0]+contour1_ellipse[1][1], contour2_ellipse[1][0]+contour2_ellipse[1][1])

print "areas", cv2.contourArea(mergedContours[x]), cv2.contourArea(mergedContours[y])
temp_contour = np.concatenate((mergedContours[x], mergedContours[y]))
hull = cv2.convexHull(temp_contour)
print "xy_area = ", xy_area(hull)
print "cv2.contourArea = ", cv2.contourArea(hull)
tmp_img = cv2.imread(sys.argv[1])
cv2.drawContours(tmp_img, np.array([hull]), -1, (0, 255,0), 1)
cv2.imwrite(cwd+'/contour_overlay/test_contour.jpg', tmp_img)

hull_rect = cv2.minAreaRect(hull)
print "rotated rectangle area = ", hull_rect[1][0] * hull_rect[1][1]
rect = cv2.boxPoints(hull_rect)
box = np.int0(rect)
tmp_img = cv2.imread(sys.argv[1])
cv2.drawContours(tmp_img, [box], -1, (0, 255,0), 1)
cv2.imwrite(cwd+'/contour_overlay/test_rect_contour.jpg', tmp_img)

(x, y), radius = cv2.minEnclosingCircle(hull)
center = (int(x), int(y))
radius = int(radius)
print "minEnclosingCircle area = ", 3.14*(radius ** 2)
tmp_img = cv2.imread(sys.argv[1])
cv2.circle(tmp_img,center,radius,(0,255,0),1)
cv2.imwrite(cwd+'/contour_overlay/test_circ_contour.jpg', tmp_img)

ellipse = cv2.fitEllipse(hull)
print "fitEllipse area = ", 3.14*(ellipse[1][0]/2)*(ellipse[1][1]/2)
tmp_img = cv2.imread(sys.argv[1])
cv2.ellipse(tmp_img, ellipse,(0,255,0),1)
cv2.imwrite(cwd+'/contour_overlay/test_ellipse_contour.jpg', tmp_img)"""

for i in range(0, len(mergedContours)):
    rr, rg, rb = random.random(), random.random(), random.random()
    r, g, b = 0,0,0
    if rr > 0.66:
        r = 255
    elif rr > 0.33:
        r = 200
    if rg > 0.66:
        g = 200
    elif rg > 0.33:
        g = 200
    if rb > 0.66:
        b = 255
    elif rb > 0.33:
        b = 200
    cv2.drawContours(img, mergedContours, i, (r,g,b), 1)

cv2.imwrite(cwd+'/contour_overlay/'+img_name+'_contour.jpg', img)
