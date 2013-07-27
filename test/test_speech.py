from ctypes import cdll, c_int , c_char_p , c_double

# Speech Verify Engine initialize
sv_dll = cdll.LoadLibrary("../sv/libsv.so")
sv_dll.SVtrain.argtypes = [c_char_p , c_char_p , c_char_p , c_char_p , c_char_p]
sv_dll.SVdetect.argtypes = [c_char_p , c_char_p , c_char_p , c_double , c_int]
sv_dll.SVdetect.restype = c_double

def SVtrain(file1 , file2 , file3 , uid):
	try:
		ret = sv_dll.SVtrain("./sv/sv.0.0.3.2.bin" , "./static/audio_mod/%s.bin" % (uid) , file1 , file2 , file3)
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
		ret = sv_dll.SVdetect("./sv/sv.0.0.3.2.bin" , "./static/audio_mod/%s.bin" % (uid) , filename , 0.7 ,1)
		return ret
	except:
		return "error:-1;info:failure in detect"

