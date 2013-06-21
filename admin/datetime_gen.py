import datetime
if __name__=="__main__":
	now = datetime.datetime.now()
	print now
	for i in range(20):
		now=now + datetime.timedelta(days=10)
		print now
		now=now + datetime.timedelta(hours=10)
		print now
		now=now + datetime.timedelta(seconds=173)
		print now