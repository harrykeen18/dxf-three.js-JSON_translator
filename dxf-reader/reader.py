def end_three():
	file = open("three.txt",'a')
	file.write('\ngeometry = new THREE.ShapeGeometry( shape );\n')
	file.write('geometry = shape.extrude( { amount: -thickness, bevelEnabled: false } );\n')
	file.write('mesh = new THREE.Mesh( geometry, material );\n')
	file.write('mesh.position.set( 0, 0, 0 );\n')  # mesh position is based on the origin at 0,0
	file.write('scene.add( mesh );\n\n')


def start_three():

	if 'no_feat' not in locals():
		no_feat = 0

	no_feat += 1

	file = open("three.txt",'a')
	file.write('// asset ' + str(no_feat) + '\n\n')
	file.write('shape = new THREE.Shape();\n\n')


def write_three(x, y, b):

	file = open("three.txt",'a')
	file.write('shape.moveTo( ' + str(x) + ', ' + str(y) + ');\n')

	# file.write(str(x) + ' ' + str(y) + ' ' + str(b) + '\n')


def import_scan():
	
	# overwrite old three.txt file
	file = open("three.txt",'w')
	file.close

	import_list = open("real.dxf").readlines()
	print len(import_list)
	# remove all \n from strings
	for n, i in enumerate(import_list):
		if "\n" in i:
			import_list[n] = i.replace('\n','')

	# start scaning list for lines and stuff.
	for n, i in enumerate(import_list):

		if "POLYLINE" in i:

			# write first lines for a new part
			start_three()

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
							#bulge = float(import_list[v + 7])
							bulge = 0.0

							print x
							print y
							print bulge

							write_three(x, y, bulge)
						
						# if "10" in import_list[v] and "20" in import_list[v + 2]:
						# 	print "10 " + import_list[v + 1]
						# if "20" in import_list[v] and "30" in import_list[v + 2]:
						# 	print "20 " + import_list[v + 1]
						# if "42" in import_list[v] and "0" in import_list[v + 2]:
						#	print "42 " + import_list[v + 1]


			# write first lines for a new part
			end_three()

if __name__ == '__main__':
	import_scan()