from shapely.geometry import Point, Polygon

#function to check if a centrepoint of a bounding box is inside a polygon
def compare_polygon_bbox(centre_point, polygon_points):
    """ 
    Inputs:
        centre_point: tuple of (x,y) coordinates of the centre point of the bounding box
        polygon_points: list of tuples of (x,y) coordinates of the polygon
    Output:
        True if the centre point is inside the polygon, False otherwise
    """
    #create a polygon object
    polygon = Polygon(polygon_points)
    #create a point object
    point = Point(centre_point)
    #check if the point is inside the polygon
    if point.within(polygon):
        return True
    return False


poly_points = [
    (  7.277622,  133.61368  ),
 (  9.231773,  126.277084 ),
 ( 11.324226,  118.60668  ),
 ( 15.393163 , 110.37749  ),
 ( 19.701317  ,100.93622  ),
 ( 24.183994  , 91.74154  ),
 ( 29.614468  , 83.484245 ),
 ( 35.237103  , 76.68334  ),
 ( 40.527405  , 68.889565 ),
 ( 47.028866  , 62.732716 ),
 ( 54.76698   , 55.042713 ),
 ( 61.856354  , 49.238384 ),
 ( 69.824165  , 42.484398 ),
 ( 77.56974   , 37.136158 ),
 ( 85.82248   , 31.774902 ),
 ( 93.51531   , 27.437622 ),
 (100.92112   , 23.699112 ),
 (109.86892   , 19.765884 ),
 (117.508255  , 16.632969 ),
 (125.05255   , 14.537648 ),
 (133.13985   , 11.680146 ),
 (141.15865   ,  8.410972 ),
 (149.33708   ,  6.122151 ),
 (157.3376    ,  4.337572 ),
 (164.0353    ,  2.0673144),
 (186.36147   , 48.44304  ),
 (177.22803   , 50.86712  ),
 (170.44899   , 52.685333 ),
 (163.25601   , 54.22199  ),
 (155.859     , 56.22735  ),
 (149.05484   , 58.90281  ),
 (142.66284   , 61.30395  ),
 (136.91966   , 64.51954  ),
 (129.58873   , 67.956924 ),
 (123.907486  , 71.04297  ),
 (118.15451   , 75.06636  ),
 (112.01609   , 78.805916 ),
 (105.36265   , 83.24034  ),
 ( 98.84395   , 88.36077  ),
 ( 93.58247   , 92.91719  ),
 ( 88.20839   , 99.2035   ),
 ( 82.9266    ,104.692726 ),
 ( 77.96761   ,110.44139  ),
 ( 73.7692    ,116.33732  ),
 ( 69.53552   ,123.05418  ),
 ( 66.62977   ,129.62024  ),
 ( 64.02417   ,137.04929  ),
 ( 61.49178   ,143.70456  ),
 ( 60.23151   ,150.03653  ),
 ( 56.852757  ,154.66925  ),
]

# plot the polygon points on an image and save it
# import cv2
# import numpy as np
# image = cv2.imread("172_DENVER.jpg")
# for polygon in poly_points:
#     pts = np.array(polygon, np.int32)
#     pts = pts.reshape((-1, 1, 2))
#     cv2.polylines(image, [pts], isClosed=True, color=(255, 0, 0), thickness=2)

# #saver it as a new image
# cv2.imwrite("172_DENVER_polygons.jpg", image)



centre_point = (40.527405,68.889565)
res = compare_polygon_bbox(centre_point, poly_points)
print(res)