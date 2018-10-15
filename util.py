### Functions used for obj_count.py
import numpy as np
import cv2

def xy_area(points):
    #rectangular area
    x = [point.item(0) for point in points]
    y = [point.item(1) for point in points]
    l_f = max(x)
    w_f = max(y)
    l_i = min(x)
    w_i = min(y)
    return (l_f - l_i)*(w_f - w_i)

def max_xy(points):
    x = [point.item(0) for point in points]
    y = [point.item(1) for point in points]
    return max(x), max(y)

def distance(pt1, pt2):
    return ((pt1[0][0]-pt2[0][0]) ** 2 + (pt1[0][1]-pt2[0][1]) ** 2)**0.5

def over_lapping(points, img_covered):
    x = [point.item(0) for point in points]
    y = [point.item(1) for point in points]
    l_f = max(x)
    w_f = max(y)
    l_i = min(x)
    w_i = min(y)
    if img_covered[w_f][l_i] or img_covered[w_i][l_i] or img_covered[w_f][l_f] or img_covered[w_i][l_f]:
        return True
    else:
        for r in range(w_i, w_f+1):
            for c in range(l_i, l_f+1):
                img_covered[r][c] = 1
        return False

def reject_outliers(data, m=2):
    return data[abs(data - np.mean(data)) < m * np.std(data)]

def stats(contours, area, bot_thresh, top_thresh):
    """contours = list of contours, area = area function to eval contours,
        bot_thresh = lower threshold value, top_thresh = upper threshold value"""
    area = [area(contour) for contour in contours if area(contour) > bot_thresh and area(contour) < top_thresh]
    area_np = np.array(area)
    area_np = reject_outliers(area_np)
    print "Min area:", min(area_np)
    print "Max area:", max(area_np)
    mean = np.mean(area_np)
    print "Mean area:",mean
    print "Median area:",np.median(area_np)
    std = np.std(area_np)
    print "STD:",std
    return np.median(area_np)
    #Buckets
    """print "10% Bucket:",len([a for a in area_np if a < max(area_np)*0.1])
    print "20% Bucket:",len([a for a in area_np if a >= max(area_np)*0.1  and a < max(area_np)*0.2])
    print "30% Bucket:",len([a for a in area_np if a >= max(area_np)*0.2  and a < max(area_np)*0.3])
    print "40% Bucket:",len([a for a in area_np if a >= max(area_np)*0.3  and a < max(area_np)*0.4])
    print "50% Bucket:",len([a for a in area_np if a >= max(area_np)*0.4  and a < max(area_np)*0.5])
    print "60% Bucket:",len([a for a in area_np if a >= max(area_np)*0.5  and a < max(area_np)*0.6])
    print "70% Bucket:",len([a for a in area_np if a >= max(area_np)*0.6  and a < max(area_np)*0.7])
    print "80% Bucket:",len([a for a in area_np if a >= max(area_np)*0.7  and a < max(area_np)*0.8])
    print "90% Bucket:",len([a for a in area_np if a >= max(area_np)*0.8  and a < max(area_np)*0.9])
    print "100% Bucket:",len([a for a in area_np if a >= max(area_np)*0.9])"""

def merging(contours, area_thresh, dist_thresh, px_mm):
    mergedContours = []
    alreadyMerged = {}
    #Initialize alreadMerged
    for i in range(0, len(contours)):
        alreadyMerged[i] = False
    for i in range(0, len(contours)):
        contour1 = contours[i]
        for j in range(0, len(contours)):
            contour2 = contours[j]
            temp_contour = np.concatenate((contour1, contour2))
            hull = cv2.convexHull(temp_contour)
            #Need at least 4 points in the hull to compute ellipse
            if i != j and not alreadyMerged[i] and not alreadyMerged[j] and \
            len(contour1) > 4 and len(contour2) > 4 and len(hull) > 4:
                ellipse = cv2.fitEllipse(hull)
                contour1_ellipse = cv2.fitEllipse(contour1)
                contour2_ellipse = cv2.fitEllipse(contour2)
                hull_ellipse_area = ellipse_area(ellipse)
                cross_dist = max(dist_thresh*px_mm, contour1_ellipse[1][0]+contour1_ellipse[1][1], contour2_ellipse[1][0]+contour2_ellipse[1][1])
                if distance(centroid(contour1), centroid(contour2)) < cross_dist  \
                  and abs(hull_ellipse_area - cv2.contourArea(hull))/hull_ellipse_area < area_thresh:
                    mergedContours += [temp_contour]
                    alreadyMerged[i] = True
                    alreadyMerged[j] = True
                    print i, j
    for i in range(0, len(contours)):
        if not alreadyMerged[i]:
            mergedContours += [contours[i]]
    return mergedContours

def centroid(contour):
    M = cv2.moments(contour)
    center = [[M['m10']/M['m00'], M['m01']/M['m00']]]
    #print center
    return center

def ellipse_area(ellipse):
    return 3.14*(ellipse[1][0]/2)*(ellipse[1][1]/2)
