Mobile CheckIn 移动签到
============================
----------------------------
Quick Start
----------------------------

Three quick start options are available:

- Download the latest release.
- Clone the repo: `git clone git://github.com/SweenEy1130/MobileCheckIn.git`.
- Install MySQL,Tornado 2.4.1.
- Run `init.sql` to initialize database;
- Run the command `python main.py` to start the server

文件列表
----------------------------

- `face.py` 		人脸识别模块
- `facepp.py` 	Face++ SDK
- `basic.py` 	基本模块-验证和基本登录
- `main.py` 		主程序
- `SQL.txt` 		MySQL初始化语句
- `location.py`	地理位置注册和验证
- `sv.py`		语音注册和验证
- `admin.py`		后台管理界面模块
- `jaccount.py`	Jaccount SDK
- `jalogin.py`	Jaccount登录模块
- `gps.py`		运算地理距离
- `settings.py`	系统设置-端口和IP
- `init.sql`		MySQL初始化配置
- `config.conf`	服务器配置文件


API文档
----------------------------
###登陆界面###
- API:    `POST http://domain:port/login`
- POST:   `{'name':'xxx','password':'xxx'}`
- HEADER:  `{  "Content-type":"application/json",
            "Accept":"text/plain",
            "Connection": "Keep-Alive", 
            "Cache-Control": "no-cache" }`
- RESPONSE:`{"error":0}`
- ERROR CODE:  

 		0 for success
        1 for invalid password
        2 for password or username can't be empty

###用户注册###
- API:    `POST http://domain:port/login`
- POST   `{'name':'xxx','password':'xxx'}`
- HEADER `{"Content-type":"application/json",
        "Accept":"text/plain",
        "Connection": "Keep-Alive", 
        "Cache-Control": "no-cache" }`
- RESPONSE:`{"error":}`
- ERROR CODE:

		0 for success
        1 for username exist
        2 for password or username can't be empty

### 查询用户注册状态 ###
- API:` GET http://domain:port/checkstatus`
- HEADER:  `{  "Content-type":"application/json",
            "Accept":"text/plain",
            "Connection": "Keep-Alive", 
            "Cache-Control": "no-cache",
            "Cookie": client_cookie }`
- RESPONSE:`{"error":0}`
- ERROR CODE:  


 		0 for success
        1 for not login
        2 for SQL error


### 面部验证 ###
- API `http://domain:port/faceverify`
- POST:	`{"pic":picture_file}`
- HEADER:  `{  "Accept":"application/json",
			"Connection": "Keep-Alive", 
			"Cache-Control": "no-cache" ,
			"Cookie": client_cookie}`
- RESPONSE: `{"error":,"similarity":}`
- ERROR CODE:	

		0 for success
		1 for face unrecogize
		2 for not login
- Cookie should contain the response set-cookie from the sever when user login(important!)


### 面部注册 ###
- API `POST http://domain:port/faceregister`
- POST:	`{"pic":picture_file}`
- HEADER:  `{  "Accept":"application/json",
			"Connection": "Keep-Alive", 
			"Cache-Control": "no-cache" ,
			"Cookie": client_cookie}`
- RESPONSE:`{  "error":,"faceid":}`
- ERROR CODE:	
		
		0 for success
		1 for face unrecogized
		2 for not login
		3 for face_add error
		4 for already register
- Cookie should contain the response set-cookie from the sever when user login(important!)
the `client_cookie` can get from the server's response

### 语音训练 ###
- API `POST http://domain:port/svtrain`
- POST:`	{"voice1":voice,"voice2":voice,"voice3":voice}`
- HEADER:  `{  "Accept":"application/json",
			"Connection": "Keep-Alive", 
			"Cache-Control": "no-cache" ,
			"Cookie": client_cookie}`
- RESPONSE:`{"error":}`
- ERROR CODE:	

		0 for success
		1 for not login
		2 for newSVEngine error
		3 for speaker adapt model failed
		-1 for failure in train
- 备注：上传语音格式：wav格式8000hz 16bit mono

### 语音验证 ###
- API `POST http://domain:port/svdetect`
- POST:	`{"voice":voice}`
- HEADER:  `{  "Accept":"application/json",
			"Connection": "Keep-Alive", 
			"Cache-Control": "no-cache" ,
			"Cookie": client_cookie}`
- RESPONSE:`{"error":}`
- ERROR CODE:

		0 for success
		1 for not login
		2 for not accepted
		4 for user not initialize audio
		-1 for failure in detect process

### 地理位置上传 ###
- API `POST http://domain:port/uploadlocation`
- POST:	`{'latitude':latitude,'longitude':longitude}`
- HEADER:  `{  "Accept":"application/json",
            "Connection": "Keep-Alive", 
            "Cache-Control": "no-cache" ,
            "Cookie": client_cookie}`

### 地理位置注册 ###
- API `POST http://domain:port/registerlocation`
- POST:	`{'locid':1}`
- HEADER:  `{ "Accept":"application/json",
            "Connection": "Keep-Alive", 
            "Cache-Control": "no-cache" ,
            "Cookie": client_cookie}`
- 备注：目前仅有SJTU，locid为1

### 创建验证 ###
- API `POST http://domain:port/detectcreate`
- HEADER:  `{  "Accept":"application/json",
            "Connection": "Keep-Alive", 
            "Cache-Control": "no-cache" ,
            "Cookie": client_cookie}`
- RESPONSE:`{"error": }`
- ERROR CODE:  
 
 		0 for success
        1 for SQL error
        2 for not login
- 返回set-cookie新增sessionid，需加入到http协议的cookie中



### 查询验证结果 ###
- API `POST http://domain:port/getdetectresult`
- HEADER: `{  "Accept":"application/json",
            "Connection": "Keep-Alive", 
            "Cache-Control": "no-cache" ,
            "Cookie": client_cookie}`
- RESPONSE:  `{"error": 0}`
- ERROR CODE:  
 
		0 for success
        1 for fail
        2 for not login
        3 for no sessionid
     	4 for SQL error0 for success
        5 for SQL error
        6 for not enough detect info

