# coding=gbk
# $File: gps.py
# $Date: Wed May 8 1:09:27 2013 +0800
# $Author: ronnie.alonso@gmail.com
#
#      0. You just DO WHAT THE FUCK YOU WANT TO. 

import math
from decimal import Decimal
"""
GPS function
"""
def deg2rad(d):
		return d*math.pi/180.0
def spherical_distance(f, t):
	"""
	calc distance from two point
	#Frompoint = [latitude,longitude]
	#g=GPS()
	#print g.spherical_distance(frompoint,topoint)
	"""
	EARTH_RADIUS_METER =6378137.0;
	flon = deg2rad(f[1])
	flat = deg2rad(f[0])
	tlon = deg2rad(t[1])
	tlat = deg2rad(t[0])
	con = math.sin(flat)*math.sin(tlat)
	con += math.cos(flat)*math.cos(tlat)*math.cos(flon - tlon)
	return round(math.acos(con)*6378137.0/1000,4)

if __name__ == "__main__":
	f = [31.236797 , 121.475886]
	d = [39.915599 , 116.393058]
	print spherical_distance(f,d)