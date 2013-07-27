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

if __name__ == '__main__':

	userlist = []

	os.chdir("identical")

	
	for filename in glob.glob("*.wav"):
		uid = filename[0:5]
		print userlist
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
