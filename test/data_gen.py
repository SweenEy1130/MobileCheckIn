import datetime
import random
lat=31.030316
lng=121.439595
def ram_int(now):
	i=random.randint(0,50)
	j=random.randint(0,50)
	lat_span = 0.00223234 * (i-25)+31.030316;
	lng_span = 0.00243543 * (j-25)+121.439595;
	item={'LONGITUDE':lng_span,'LATITUDE':lat_span,'DETECTTIME':now}
	return item

if __name__=="__main__":
	data = []
	now = datetime.datetime.now()
	data.append(ram_int(now))
	for i in range(100):
		now=now + datetime.timedelta(seconds=-173)
		data.append(ram_int(now))
		now=now + datetime.timedelta(days=-1)
		data.append(ram_int(now))
		now=now + datetime.timedelta(hours=7)
		data.append(ram_int(now))
		now=now + datetime.timedelta(seconds=173)
		data.append(ram_int(now))
	output = open('location.data', 'w')
	for item in data:
		sql='INSERT INTO DETECT(OWNER,LONGITUDE,LATITUDE,DETECTTIME) VALUES (,%s,%s,\'%s\');' %(item['LONGITUDE'],item['LATITUDE'],item['DETECTTIME'])
		output.write(sql+'\n')