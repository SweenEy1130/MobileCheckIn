import datetime
import random
lat=31.027121
lng=121.437825
def ram_int(now):
	i=random.randint(0,50)
	j=random.randint(0,50)
	lat_span = 0.00023234 * (i-25)+31.030316;
	lng_span = 0.00033543 * (j-25)+121.439595;
	item={'LONGITUDE':lng_span,'LATITUDE':lat_span,'DETECTTIME':now.strftime('%Y-%m-%d %H:%M:%S')}
	return item

if __name__=="__main__":
	data = []
	now = datetime.datetime.now()
	data.append(ram_int(now))
	for i in range(50):
		now=now + datetime.timedelta(days=-3)
		data.append(ram_int(now))
		now=now + datetime.timedelta(hours=9)
		data.append(ram_int(now))
		now=now + datetime.timedelta(seconds=93)
		data.append(ram_int(now))
		now=now + datetime.timedelta(days=-7)
		data.append(ram_int(now))
	output = open('detect.sql', 'w')
	uid =[5100309582,5100809149]
	for item in data:
		owner = uid[random.randint(0,1)]
		sql='INSERT INTO DETECT(OWNER,LONGITUDE,LATITUDE,DETECTTIME,STATUS) VALUES (%s,%s,%s,\'%s\',0);' %(owner,item['LONGITUDE'],item['LATITUDE'],item['DETECTTIME'])
		output.write(sql+'\n')
