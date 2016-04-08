
import_list = open("test.dxf").readlines()

for n, i in enumerate(import_list):
	if "\n" in i:
		import_list[n] = i.replace('\n','')

for n, i in enumerate(import_list):

	if "POLYLINE" in i:

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

				print "STARTTTTTTTTTTTTTT"
				for v in range(polyline_ind, v_end):
					
					if "10" in import_list[v] and "20" in import_list[v + 2]:
						print "10 " + import_list[v + 1]
					if "20" in import_list[v] and "30" in import_list[v + 2]:
						print "20 " + import_list[v + 1]
					if "42" in import_list[v] and "0" in import_list[v + 2]:
						print "42 " + import_list[v + 1]
				print "ENDDDDDDDDDDDDDDDD"