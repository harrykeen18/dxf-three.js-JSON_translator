import math
import numpy as np
import operator

# A function to work out the webgl type co-ordinates of a 
# fillet between two lines from a dxf. Fillet of known start
# A and end B with a known bulge factor. Must find radius of
# fillet and center point.

#      C o-------o D
# A o
#    \
#     \
#      \
#       o B

bulge = - 1.1716/2.8284
Ax = 9.1716
Ay = 9.1716
Bx = 0.0
By = 0.0
Cx = 14.8284
Cy = 9.1716
Dx = 24.0
Dy = 0.0

A = np.array([Ax, Ay])
B = np.array([Bx, By])
C = np.array([Cx, Cy])
D = np.array([Dx, Dy])

# find theta between AB and CD

AB = B - A
CD = D - C

#print AB
#print CD

theta = math.acos((np.dot(AB, CD))/(np.linalg.norm(AB) * np.linalg.norm(CD)))
#print theta * 360/(2 * math.pi)

# find distance between A and C

d = math.sqrt(math.pow((Ax - Cx), 2) + math.pow((Ay - Cy), 2) )
#print "d " + str(d)

# find height of arc

h = bulge * d/2
#print "h " + str(h)

#find radius

r = h/2 + math.pow(d, 2)/(8 * h)
#print "r " + str(r)

# find circle intersections from A and C with rad of r

# find mid point between A and C

xm = Ax + (Cx - Ax) / 2
ym = Ay + (Cy - Ay) / 2
#print xm, ym

# find dist. to fillet center point from midpoint

cd = math.sqrt(math.pow(r, 2) - math.pow(d/2, 2))
#print cd

# find 2 possible intersection points

Xc1 = xm + cd * (Cy - Ay)/d
Yc1 = ym + cd * (Cx - Ax)/d

Xc2 = xm - cd * (Cy - Ay)/d
Yc2 = ym - cd * (Cx - Ax)/d


# need to choose the right combination of co-ordinates from 4 possible points

point1 = [Xc1, Yc1]
point2 = [Xc1, Yc2]
point3 = [Xc2, Yc1]
point4 = [Xc2, Yc2]

# find distance of all points to B

dpoint1 = math.sqrt(math.pow(point1[0] - Bx, 2) + math.pow(point1[1] - By, 2))
dpoint2 = math.sqrt(math.pow(point2[0] - Bx, 2) + math.pow(point2[1] - By, 2))
dpoint3 = math.sqrt(math.pow(point3[0] - Bx, 2) + math.pow(point3[1] - By, 2))
dpoint4 = math.sqrt(math.pow(point4[0] - Bx, 2) + math.pow(point4[1] - By, 2))

dpoint = {1: dpoint1, 2: dpoint2, 3: dpoint3, 4: dpoint4}
#print dpoint

# sort closest to furthest in list
sorted_dpoint = sorted(dpoint.items(), key=operator.itemgetter(1))
#print sorted_dpoint

# take the top two and see if they lie on a circle from A or C with rad r
closest_points = [x[0] for x in sorted_dpoint]
closest1 = closest_points[0]
closest2 = closest_points[1]

if closest1 == 1:
	clo_point1 = point1
elif closest1 == 2:
	clo_point1 = point2
elif closest1 == 3:
	clo_point1 = point3
elif closest1 == 4:
	clo_point1 = point4

if closest2 == 1:
	clo_point2 = point1
elif closest2 == 2:
	clo_point2 = point2
elif closest2 == 3:
	clo_point2 = point3
elif closest2 == 4:
	clo_point2 = point4

#print clo_point1
#print clo_point2

radclo1 = r - math.sqrt(math.pow(clo_point1[0] - Ax, 2) + math.pow(clo_point1[1] - Ay, 2))
radclo2 = r - math.sqrt(math.pow(clo_point2[0] - Ax, 2) + math.pow(clo_point2[1] - Ay, 2))

#print radclo1
#print radclo2

if radclo1 < radclo2:
	center_point = clo_point1
else:
	center_point = clo_point2

print center_point
print r