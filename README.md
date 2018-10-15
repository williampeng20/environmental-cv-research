# forestry-cv-research

## Log

### Week 1
Vinay: Ran an edge detector on tree cross section. Took contours. Mixed results, able to detect parts of rings, but lots of noise as well.

William: Ran Canny-Edge Detection and then found contours from binary image produced from edge detection. Results were poor, only half of objects were detected, and many contours recognized negative space or reflections.

### Week 2
Vinay: Ran Hough Circle detection on original image as well as on contoured image. Took infeasibly long to run. Ran a closing algorithm on contoured image in an attempt to complete the gaps in the tree rings. Not particularly helpful.

William: Used less dense source image, and analyzed a smaller sub section for clearer results. Updated Canny Edge detection min/max values to capture more edges, however too many edges now and need to be filtered.

### Week 3
Vinay: Took 8 cross 15 pixel wide slices of the image in a 40 degree arc, each 5 degrees apart. Ran an edge detector on each and contoured individually. Vertically stacked slices and ran a sliding window across the resulting imaging, collecting "votes" for whether each slice was able to yield a ring there. Need to figure out how to tune parameters -- it seems like results vary pretty wildly between cross sections, may not be a good correlation with whre the rings actually exist.

William: Found the area of each contour, first using cv.contourArea() but had problems since many contours are sparse in width but have are long, so found rectangular area. Also implemented an overlapping function to prevent contours from stacking on each others' space. Finally, found statistics and buckets on the area of all the final pruned contours.

### Week 4
William: Ran approxPolyDP on contours found to approximate polygons to close lines, and then merged contours if their endpoints matched up. Tried using convexHull but it didn't work well with contours that had extraneous points outside of the object. Finally, I threw out contours with area under the median area, since about half of the contours were in the 10% bucket in area.

### Week 5
William: Implemented millimeter to pixel ratio, with knowledge that petri dish has a 14cm diameter and sieve gets items of 1-5mm size. Furthermore added multicoloring to contour drawing to clarify visual results. Still adjusting parameters in merging contours.

### Week 6
William: Merging contours rewritten - compare pairs of contours, and merge if the convexHull is similar to the ellipse of the pair (More specifically, if the area difference normalized by the area of the ellipse is less than the specified area threshold). Another condition is that the center's of both contours should be near each other, at least the distance specified by a distance threshold or the sum of an individual contour's ellipse axis' lengths. During merging, only allow a contour to be merged once for that function call. Thus, I call the merge function multiple iterations, which should be the maximum amount of fragmented contours for any object in the image.
