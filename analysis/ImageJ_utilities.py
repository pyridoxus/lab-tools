"""Miscellaneous utilities for python interaction with ImageJ"""
_rcsid="ImageJ_utilities.py,v 1.3 2003/05/30 13:31:54 mendenhall Release-20050805"

def read_ImageJ_measurement_file(file, maxlen=1000000):
	"Read a measurements file from ImageJ, and return a dictionary mapping columns names to numbers, a list of column names, and a table of the data provided"
	f=open(file,"r")
	strings=f.read(maxlen).split("\n")
	f.close()
	columns=[ [i.strip() for i in line.split("\t")] for line in strings if line]
	header=columns[0]
	keys={}
	#extract column names
	for i in range(1,len(header)):
		keys[header[i]]=i
	return keys, columns[0][1:], columns[1:]

def read_ImageJ_roi_file(file):
	"Read a measurements file from ImageJ containing  (at least) the bounding rectangle information for a series of ROIs"
	keys, column_names, data = read_ImageJ_measurement_file(file)
	rois=[]
	column_map=[keys[name] for name in ("BX","BY","Width","Height")] 
	for i in data[1:]:
		x0, y0, width, height= [int(i[c]) for c in column_map] 
		rois.append([x0,y0,x0+width,y0+height])
	return rois
 
