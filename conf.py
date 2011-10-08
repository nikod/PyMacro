#!/usr/bin/python2

def Read():
	config = open('config', "r")
	A = []
	while True:
		temp1 = config.readline().rsplit(" =")
		if temp1 != [""]:
			temp2 = temp1[1].split()
			B = {"Name" : temp1[0], "Type" : temp2[0], "Macro" : temp2[1]}
			A.append(B)
		else:
			break
	config.close()
	return A
