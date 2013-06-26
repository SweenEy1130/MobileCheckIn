# coding=gbk
from ctypes import cdll, c_int , c_char_p , c_double

if __name__ == "__main__":
	sv_dll = cdll.LoadLibrary("./libsv.so")
	sv_dll.SVtrain.argtypes = [c_char_p , c_char_p , c_char_p]
	sv_dll.SVdetect.argtypes = [c_char_p , c_char_p , c_char_p , c_double , c_int]
	sv_dll.SVdetect.restype = c_double
	ret = sv_dll.SVtrain("sv.0.0.3.2.bin" , "test.bin" , "1.wav")
	print "train:",ret
	conf = sv_dll.SVdetect("sv.0.0.3.2.bin" , "test.bin", "2.wav" , 1 , 1)
	print "detect:",conf
