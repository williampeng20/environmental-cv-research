### Functions used for obj_count.py
import numpy as np

def xy_area(points):
    #rectangular area
    x = [point.item(0) for point in points]
    y = [point.item(1) for point in points]
    l_f = max(x)
    w_f = max(y)
    l_i = min(x)
    w_i = min(y)
    return (l_f - l_i)*(w_f - w_i)

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
