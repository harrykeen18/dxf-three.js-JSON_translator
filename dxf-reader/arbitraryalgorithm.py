import math
import numpy as np

# Here we are looking for the arbitrary X and Y axes to go with the normal N.
# They will be called Ax and Ay. N could also be called Az (the arbitrary Z axis) as follows:

# N is the value defined by 210, 220 and 230 in DXF language

# for the example N is 210
# 0.7071067811865472

# -0.7071067811865479

# 0.0

# If (abs (Nx) < 1/64) and (abs (Ny) < 1/64) then 
#    Ax = Wy X N (where "X" is the cross-product operator). 
# Otherwise, 
#    Ax = Wz X N. 
# Scale Ax to unit length.

# The method of getting the Ay vector is:

# Ay = N X Ax. Scale Ay to unit length.

def cross(a, b):
    c = [a[1]*b[2] - a[2]*b[1],
         a[2]*b[0] - a[0]*b[2],
         a[0]*b[1] - a[1]*b[0]]

    return c

def run_test():
	xWCS = [1, 0, 0]
	yWCS = [0, 1, 0]
	zWCS = [0, 0, 1]
	N = [0.7071067811865472, -0.7071067811865479, 0.0]

	if math.sqrt(math.pow(N[0], 2)) < 1/64 and math.sqrt(math.pow(N[1], 2)) < 1/64:
		Ax = cross(yWCS, N)
	else:
		Ax = cross(zWCS, N)

	Ay = cross(N, Ax)

	print Ax
	print Ay

	# build new co-ord system matrix
	new_coord_sys = [Ax, Ay, N]
	# new_coord_sys = [[0, 0, 1], [0, 1, 0], [2, 0, 0]]

	print new_coord_sys
	
	# find inverse co-ord system as transfer matrix
	INV_new_coord_sys = np.linalg.inv(new_coord_sys)
	print INV_new_coord_sys

	point2 = np.dot(INV_new_coord_sys, np.dot([xWCS, yWCS, zWCS], [400, 800, 0]))
	print point2

	# Dot-product multiply the vector by the
	# first column to get the transformed X, second column to get the transformed Y, etc.

	# INV_ROW_1 = INV_new_coord_sys[0]
	# INV_ROW_2 = INV_new_coord_sys[1]
	# INV_ROW_3 = INV_new_coord_sys[2]

	# INV_COL_1 = [INV_ROW_1[0], INV_ROW_2[0], INV_ROW_3[0]]
	# INV_COL_2 = [INV_ROW_1[1], INV_ROW_2[1], INV_ROW_3[1]]
	# INV_COL_3 = [INV_ROW_1[2], INV_ROW_2[2], INV_ROW_3[2]]

	# print INV_COL_1
	# print INV_COL_2
	# print INV_COL_3

	# test_point = [830,2276,0]

	# x = np.dot(test_point, INV_COL_1)
	# y = np.dot(test_point, INV_COL_2)
	# z = np.dot(test_point, INV_COL_3)

	# print x
	# print y
	# print z



if __name__ == '__main__':
	run_test()