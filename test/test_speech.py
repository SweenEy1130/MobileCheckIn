from ctypes import cdll, c_int , c_char_p , c_double

# Speech Verify Engine initialize
sv_dll = cdll.LoadLibrary("../sv/libsv.so")
sv_dll.SVtrain.argtypes = [c_char_p , c_char_p , c_char_p , c_char_p , c_char_p]
sv_dll.SVdetect.argtypes = [c_char_p , c_char_p , c_char_p , c_double , c_int]
sv_dll.SVdetect.restype = c_double

def SVtrain(uid , file1 , file2 , file3):
	try:
		ret = sv_dll.SVtrain3("../sv/sv.0.0.3.2.bin" , "audio_mod/%s.bin" % (uid) , file1 , file2 , file3)
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
		ret = sv_dll.SVdetect("../sv/sv.0.0.3.2.bin" , "audio_mod/%d.bin" % (uid) , filename , 0.7 ,1)
		return ret
	except:
		return "error:-1;info:failure in detect"

if __name__ == '__main__':
	ret = SVtrain(5101109071 , "audio/51011090711578985057.wav" , "audio/51011090711578985345.wav" , "audio/51011090711578985516.wav")
	print ret

	ret = SVdetect(5101109071 , "audio/51011090711578985057.wav")
	print ret
