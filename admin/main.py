# coding=utf-8
import tornado.ioloop,tornado.web,tornado.httpserver,tornado.database,tornado.options
from admin import TimeQueryHandler,TimeHandler,MapQueryHandler,MapHandler,SettingHandler,DeleteAdminHandler,ManageHandler,RuleHandler,adminHandler,JaLoginHandler,JaLogoutHandler, StudentHandler, StudentEditHandler,CheckHandler
import os
from tornado.options import define,options
define("port", default=8000, help="run on the given port", type=int)

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r"/admin", adminHandler),
			(r"/admin/jalogin" , JaLoginHandler),
			(r"/admin/logout" , JaLogoutHandler),
			(r"/admin/student", StudentHandler),
			(r"/admin/student/edit", StudentEditHandler),
			(r"/admin/checkin",CheckHandler),
			(r"/admin/rule", RuleHandler),
			(r"/admin/manage", ManageHandler),
			(r"/admin/manage/delete", DeleteAdminHandler),
			(r"/admin/setting", SettingHandler),
			(r"/admin/map_stat", MapHandler),
			(r"/admin/map_stat/search", MapQueryHandler),
			(r"/admin/time_stat", TimeHandler),
			(r"/admin/time_stat/([0-9]+)", TimeQueryHandler),
		]
		settings = dict(
			debug = True,
			template_path = os.path.join(os.path.dirname(__file__), "templates").encode("gbk"), 
			static_path = os.path.join(os.path.dirname(__file__), 'static').encode("gbk"),
			cookie_secret = "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E="
		)
		tornado.web.Application.__init__(self , handlers , **settings)
		self.db = tornado.database.Connection(host = 'localhost:3306' , database= 'mobile' , user = 'root' , password = '')

if __name__ == "__main__":
	print "Welcome to Mobile Checkin Server"
	# tornado.options.parse_config_file("config.conf")
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()