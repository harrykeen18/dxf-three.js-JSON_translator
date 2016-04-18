import math
import numpy as np
import os

BLANKPAGE = 'gen3_lineto.html'
NEWPAGE = 'NEW_gen3_lineto.html'
HTMLLIST = []
DXFFILE = '..\\dxfs\\test3d_comp.dxf'# 'C:\Users\Harry\Documents\GitHub\dxf-three.js-JSON_translator\dxf-reader\dxfs\\test3d.dxf'

def angle_vec(WCS_axis, arb_axis):

	# finds abgle between two vectors
	theta = math.acos((np.dot(WCS_axis, arb_axis))/(np.linalg.norm(WCS_axis) * np.linalg.norm(arb_axis)))
	print theta * 360/(2 * math.pi)
	return theta

def cross(a, b):

	# finds cross product between a 3x3 matrix
	c = [a[1]*b[2] - a[2]*b[1],
		a[2]*b[0] - a[0]*b[2],
		a[0]*b[1] - a[1]*b[0]]

	return c

def find_arb_axes(Az):

	# Finds arbritrary axes of new co-ordinate system from Autodesk's arbritrary algorithm
	# http://www.autodesk.com/techpubs/autocad/acad2000/dxf/arbitrary_axis_algorithm_dxf_ab.htm

	xWCS = [1, 0, 0]
	yWCS = [0, 1, 0]
	zWCS = [0, 0, 1]
	N = Az # [0.7071067811865472, -0.7071067811865479, 0.0]

	if math.sqrt(math.pow(N[0], 2)) < 1/64 and math.sqrt(math.pow(N[1], 2)) < 1/64:
		Ax = cross(yWCS, N)
	else:
		Ax = cross(zWCS, N)

	Ay = cross(N, Ax)

	arb_axes = [Ax, Ay]

	return arb_axes

def write_html():

	# Deletes all the script that might be betweenn insert and end and drops in each line of HTMLLIST
	with open(BLANKPAGE) as f:
		lines = f.readlines()

	f.close

	start_del = lines.index('//INSERTHERE\n') + 3
	end_del	= lines.index('//ENDHERE\n') - 1

	for i in range(start_del, end_del):
		del lines[start_del]


	for i in range(0, len(HTMLLIST)):
		# lines.insert(start_del + i, "hello\n")
		lines.insert(start_del + i, HTMLLIST[i] + '\n')


	with open(NEWPAGE, 'w') as newpage:
		for l in lines:
			# print l
			newpage.write(l)


def end_three(z, Az):

	# Adds ending code to HTMLLIST
	HTMLLIST.append('		geometry = new THREE.ShapeGeometry( shape );')
	HTMLLIST.append('		geometry = shape.extrude( { amount: 18, bevelEnabled: false } );')
	HTMLLIST.append('		mesh = new THREE.Mesh( geometry, material );')
	# HTMLLIST.append('		mesh.position.z = ' + str(z) +';')

	# Add rotation if Az is not vibing.
	if Az != None:

		# Find arbritrary axes of new system

		AxAy = find_arb_axes(Az)
		print AxAy[0]
		print AxAy[1]
		print Az

		# angle between dem and dem respective WCS's

		xWCS = [1, 0, 0]
		yWCS = [0, 1, 0]
		zWCS = [0, 0, 1]

		x_rot = angle_vec(xWCS, AxAy[0])
		y_rot = angle_vec(yWCS, AxAy[1])
		z_rot = angle_vec(zWCS, Az)

		print x_rot
		print y_rot
		print z_rot

		HTMLLIST.append('		mesh.rotation.x = Math.PI / 2;')
		HTMLLIST.append('		mesh.rotation.y = Math.PI / 4;')

		# HTMLLIST.append('		mesh.rotation.set( -Math.PI / 2, -Math.PI / 2, -Math.PI / 4 )')
		# HTMLLIST.append('		mesh.rotation.set( ' + str(y_rot) + ', ' + str(y_rot) + ', '+ str(x_rot) + ' )')
		# HTMLLIST.append('		mesh.rotation.set( ' + str(x_rot) + ', ' + str(y_rot) + ', 0 )')

	HTMLLIST.append('		edges = new THREE.EdgesHelper( mesh, 0x000000 );')
	HTMLLIST.append('		scene.add( mesh );')
	HTMLLIST.append('		scene.add( edges );')

def write_three(x, y, z, bulge):

	# Adds bulk of co-ord code to HTMLLIST
	HTMLLIST.append('			shape.moveTo( ' + str(x) + ', ' + str(y) + ');')


	# Apply length parameters here
	# if z < - 100:
	# 	HTMLLIST.append('			shape.moveTo( ' + str(x) + ', ' + str(y) + ' - length/2),')
	# else:
	#  	HTMLLIST.append('			shape.moveTo( ' + str(x) + ', ' + str(y) + ' + length/2),')
	# else:
	# 	HTMLLIST.append('			new THREE.Vector3( '+ str(x) + ', ' + str(y) + ', ' + str(z) + '),')

def start_three(asset_count):

	# Adds starting code to HTMLLIST
	HTMLLIST.append('// asset ' + str(asset_count))
	HTMLLIST.append('		shape = new THREE.Shape();')

def rigid_transform_3D(A, B):

	assert len(A) == len(B)

	N = A.shape[0]; # total points

	centroid_A = mean(A, axis=0)
	centroid_B = mean(B, axis=0)

	# centre the points
	AA = A - tile(centroid_A, (N, 1))
	BB = B - tile(centroid_B, (N, 1))

	# dot is matrix multiplication for array
	H = transpose(AA) * BB

	U, S, Vt = linalg.svd(H)

	R = Vt.T * U.T

	# special reflection case
	if linalg.det(R) < 0:
	   print "Reflection detected"
	   Vt[2,:] *= -1
	   R = Vt.T * U.T

	t = -R*centroid_A.T + centroid_B.T

	print t

	return R, t

def transpose(orig_x, orig_y, orig_z, Az):
	xWCS = [1, 0, 0]
	yWCS = [0, 1, 0]
	zWCS = [0, 0, 1]
	N = Az # [0.7071067811865472, -0.7071067811865479, 0.0]

	if math.sqrt(math.pow(N[0], 2)) < 1/64 and math.sqrt(math.pow(N[1], 2)) < 1/64:
		Ax = cross(yWCS, N)
	else:
		Ax = cross(zWCS, N)

	Ay = cross(N, Ax)

	# print Ax
	# print Ay

	# build new co-ord system matrix
	new_coord_sys = [Ax, Ay, N]
	# new_coord_sys = [[0, 0, 1], [0, 1, 0], [2, 0, 0]]
	
	# find inverse co-ord system by transposing matrix
	INV_new_coord_sys = np.linalg.inv(new_coord_sys)
	# print INV_new_coord_sys

	# Translate points with this formula where
	# p2 = new point
	# M2^T = transpose of new co-ord system (3 x 3 matrix of 3 axes)
	# O1 = origin original ((0,0,0) in this case
	# O2 = origin new ((0,0,0) in this case
	# M1 = original co-ord system (3 x 3 matrix of 3 axes)
	# p1 = original point

	# p2 = M2^T dot (O1 - O2 + M1 dot p1)

	point2 = np.dot(INV_new_coord_sys, np.dot([xWCS, yWCS, zWCS], [orig_x, orig_y, orig_z]))
	# print point2

	return point2

def import_scan():

	# Imports dxf file, reads and scans for features

	asset_count = 1

	import_list = open(DXFFILE).readlines()
	# print len(import_list)
	# remove all \n from strings
	for n, i in enumerate(import_list):
		if "\n" in i:
			import_list[n] = i.replace('\n','')

	# start scaning list for lines and stuff.
	for n, i in enumerate(import_list):

		if "POLYLINE" in i:

			# write first lines for a new part
			start_three(asset_count)
			asset_count += 1

			# find index of next 'seqend' to find end of polyline feature
			p_end = 0
			p_add = 1
			p_boo = False
			while p_boo == False:
				if "SEQEND" in import_list[n + p_add]:
					p_end = n + p_add
					p_boo = True
				p_add += 1

			# print import_list[p_end]
			# print n
			# print p_end

			# find if polyline is not on x,y plane and get the Arbritrary Z axis if it isn't
			# Get index of next 'vertex' string to get snippet of code that defines the polyline
			Az = None
			# print 'Az = ' + str(Az)
			for p in range(n, n + 20):
						if "210" in import_list[p] and \
							"220" in import_list[p + 2] and \
							"230" in import_list[p + 4]:

							x = float(import_list[p + 1])
							y = float(import_list[p + 3])
							z = float(import_list[p + 5])

							Az = [x, y, z]
			print 'Az = ' + str(Az)

			point_matrix = []
			actual_points = []

			for polyline_ind in range(n, p_end):

				if "VERTEX" in import_list[polyline_ind]:

					# get index of next vertex or sequend to get indiv vertex feature
					v_end = 0
					v_add = 1
					v_boo = False



					while v_boo == False:
						if "VERTEX" in import_list[polyline_ind + v_add] or "SEQEND" in import_list[polyline_ind + v_add]:
							v_end = polyline_ind + v_add
							v_boo = True
						v_add += 1

					for v in range(polyline_ind, v_end):
						if "10" in import_list[v] and \
							"20" in import_list[v + 2] and \
							"30" in import_list[v + 4]: # and \
							#"42" in import_list[v + 6]:

							x = float(import_list[v + 1])
							y = float(import_list[v + 3])
							z = float(import_list[v + 5])
							#bulge = float(import_list[v + 7])
							bulge = 0.0

							point_matrix = np.row_stack(np.array((x,y,z)))
							print point_matrix

							if Az != None:
								actual_point = transpose(x, y, z, Az)
								actual_points = np.row_stack(actual_point)

							# print x
							# print y
							# print z
							# print bulge

							write_three(x, y, z, bulge)
						
						# if "10" in import_list[v] and "20" in import_list[v + 2]:
						# 	print "10 " + import_list[v + 1]
						# if "20" in import_list[v] and "30" in import_list[v + 2]:
						# 	print "20 " + import_list[v + 1]
						# if "42" in import_list[v] and "0" in import_list[v + 2]:
						#	print "42 " + import_list[v + 1]


				if Az != None:
					rigid_transform_3D(point_matrix, actual_points)


			# write first lines for a new part
			end_three(z, Az)
	write_html()

if __name__ == '__main__':
	import_scan()

# if __name__ == '__main__':
# 	print 'This program is being run by itself'
# else:
# 	print 'I am being imported from another module'