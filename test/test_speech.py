# coding=gbk
# $File: test_speech.py
# $Date: Sat Jul 27 18:15:27 2013 +0800
# $Author: ronnie.alonso@gmail.com
#

import os , json , glob , string , sys
from ctypes import cdll, c_int , c_char_p , c_double

# Speech Verify Engine initialize
sv_dll = cdll.LoadLibrary("../sv/libsv.so")
sv_dll.SVtrain.argtypes = [c_char_p , c_char_p , c_char_p , c_char_p , c_char_p]
sv_dll.SVdetect.argtypes = [c_char_p , c_char_p , c_char_p , c_double , c_int]
sv_dll.SVdetect.restype = c_double

def SVtrain(uid , file1 , file2 , file3):
	try:
		ret = sv_dll.SVtrain3("../../sv/sv.0.0.3.2.bin" , "../audio_mod/%s.bin" % (uid) , file1 , file2 , file3)
		# print ret
		if (ret == 1):
			return "error:1;info:newEngine error"
		elif (ret ==2):
			return "error:2;info:speaker adapt error"
		elif (ret == 0):
			return ret
	except:
		return "error:-1;info:train error"

def SVdetect(uid , filename):

	try:
		ret = sv_dll.SVdetect("../../sv/sv.0.0.3.2.bin" , "../audio_mod/%s.bin" % (uid) , filename , 0.7 ,1)
		return ret
	except:
		return "error:-1;info:failure in detect"

def CalcSimilarity(filename):
	uid = filename[0:5]
	if (uid not in userlist):
		userlist.append(uid)
		output = open("../output/%s" % uid , "w")
		output.write("%s\nFilename\tSimilarity\n" % uid)

		filepath = filename
		ret = SVtrain(uid , filepath , filepath , filepath)

		if(ret == 0):
			for cmpfile in glob.glob("*.wav"):
				cmp_id = cmpfile[0:5]

				cmp_path = cmpfile
				sim = SVdetect(uid , cmp_path)

				output.write("%s\t%s\n" % (cmp_id , sim))
		else:
			print "Train Error!\n"

		output.close()

def ThresholdStat(filename):
	input = open(filename)

	line = input.readline()
	uid = line.strip('\n')

	input.readline()

	stat =[]

	T=[]
	F=[]

	while 1:
		line = input.readline()
		line.strip('\n')
		if not line:
			break

		line = line.split('\t')

		item = {"id":line[0] , "simi":float(line[1]) * 100}

		if item["id"] == uid:
			T.append(item)
		else:
			F.append(item)

		stat.append(item)

	for thresh in range(60,80):
		T_obv = []
		F_obv = []

		for item in stat:
			if thresh <= item["simi"]:
				T_obv.append(item)

			else:
				F_obv.append(item)
			

		cnt_AD = 0
		cnt_BC = 0

		for a in T:
			for d in F_obv:
				if(a == d):
					cnt_AD += 1 

		for b in F:
			for c in T_obv:
				if(b == c):
					cnt_BC += 1

		rate_fa = cnt_BC / (len(F) * 1.0)
		rate_fr = cnt_AD / (len(T) * 1.0)

		output.write("%s's\tstatistics" % uid)
		output.write("\nThreshold\t%f" % thresh)
		output.write("\nFA rate:\t%f%%" % (rate_fa * 100))
		output.write("\nFR rate:\t%f%%\n\n" % (rate_fr * 100))

if __name__ == '__main__':

	userlist = []

	os.chdir("identical")

	
	# for filename in glob.glob("*.wav"):
	# 	CalcSimilarity(filename)

	os.chdir("../output")

	output = open("../stat","w")
	# for filename in glob.glob("*"):
	# 	ThresholdStat(filename)
	ThresholdStat("09071")
