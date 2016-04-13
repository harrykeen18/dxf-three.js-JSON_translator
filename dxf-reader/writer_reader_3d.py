import math
import numpy as np
import os

BLANKPAGE = 'gen_pagetest_3d.html'
NEWPAGE = 'NEW_gen_pagetest_3d.html'
HTMLLIST = []

def write_html():

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


def end_three():

	# delete final comma off writen line.
	# with open("three_3d.txt", 'rb+') as filehandle:
	# 	filehandle.seek(-3, os.SEEK_END)
	# 	filehandle.truncate()

	last_string = HTMLLIST[len(HTMLLIST) - 1]
	HTMLLIST[len(HTMLLIST) - 1] = last_string[:-1]

	HTMLLIST.append('		);')
	HTMLLIST.append('		var line = new THREE.Line( geometry, material );')
	HTMLLIST.append('		all_shapes.add( line )')

def write_three(x, y, z, b, Az):

	if Az != None:
		new_point = transpose(x, y, z, Az)

		x = new_point[0]
		y = new_point[1]
		z = new_point[2]

		# a = 'new_point = ' + str(new_point)
		# print a

	# Apply length parameters here
	if z < - 100:
		HTMLLIST.append('			new THREE.Vector3( '+ str(x) + ', ' + str(y) + ', ' + str(z) + ' - length/2),')
	elif z > 100:
		HTMLLIST.append('			new THREE.Vector3( '+ str(x) + ', ' + str(y) + ', ' + str(z) + ' + length/2),')
	else:
		HTMLLIST.append('			new THREE.Vector3( '+ str(x) + ', ' + str(y) + ', ' + str(z) + '),')

def start_three(asset_count):

	# file = open("three_3d.txt",'a')
	HTMLLIST.append('// asset ' + str(asset_count))
	HTMLLIST.append('		geometry = new THREE.Geometry();')
	HTMLLIST.append('		geometry.vertices.push(')


def cross(a, b):
    c = [a[1]*b[2] - a[2]*b[1],
         a[2]*b[0] - a[0]*b[2],
         a[0]*b[1] - a[1]*b[0]]

    return c


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

	# overwrite old three.txt file
	file = open("three_3d.txt",'w')
	file.close

	asset_count = 1

	import_list = open("test3d_comp.dxf").readlines()
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
			for p in range(n, n + 20):
						if "210" in import_list[p] and \
							"220" in import_list[p + 2] and \
							"230" in import_list[p + 4]:

							x = float(import_list[p + 1])
							y = float(import_list[p + 3])
							z = float(import_list[p + 5])

							Az = [x, y, z]

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

							# print x
							# print y
							# print z
							# print bulge

							write_three(x, y, z, bulge, Az)
						
						# if "10" in import_list[v] and "20" in import_list[v + 2]:
						# 	print "10 " + import_list[v + 1]
						# if "20" in import_list[v] and "30" in import_list[v + 2]:
						# 	print "20 " + import_list[v + 1]
						# if "42" in import_list[v] and "0" in import_list[v + 2]:
						#	print "42 " + import_list[v + 1]


			# write first lines for a new part
			end_three()
	write_html()

if __name__ == '__main__':
	import_scan()

# if __name__ == '__main__':
# 	print 'This program is being run by itself'
# else:
# 	print 'I am being imported from another module'