# coding=utf-8
# $File: facepp_kit.py
# $Date: Sat Jun 29 11:09:27 2013 +0800
# $Author: ronnie.alonso@gmail.com
#
#	  0. You just DO WHAT THE FUCK YOU WANT TO.

import tornado.httpclient
import itertools
import mimetools
import mimetypes

FACEPP_SERVER = "https://apicn.faceplusplus.com/v2"
API_KEY = 'b3b9061aaf64ea2515a3538dfb624e94'
API_SECRET = 'OfvW6DdyM9iqAa8TkBoBhoiWANX6Kn2Z'

# ref: http://www.doughellmann.com/PyMOTW/urllib2/
class _MultiPartForm(object):
	"""Accumulate the data to be used when posting a form."""
	def __init__(self):
		self.form_fields = []
		self.files = []
		self.boundary = mimetools.choose_boundary()
		return
	
	def get_content_type(self):
		return 'multipart/form-data; boundary=%s' % self.boundary

	def add_field(self, name, value):
		"""Add a simple field to the form data."""
		self.form_fields.append((name, value))
		return

	def add_file(self, fieldname, filename, content, mimetype = None):
		"""Add a file to be uploaded."""
		if mimetype is None:
			mimetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
		self.files.append((fieldname, filename, mimetype, content))
		return
	
	def __str__(self):
		"""Return a string representing the form data, including attached files."""
		# Build a list of lists, each containing "lines" of the
		# request.  Each part is separated by a boundary string.
		# Once the list is built, return a string where each
		# line is separated by '\r\n'.  
		parts = []
		part_boundary = '--' + self.boundary
		
		# Add the form fields
		parts.extend(
			[ part_boundary,
			  'Content-Disposition: form-data; name="%s"' % name,
			  '',
			  value,
			]
			for name, value in self.form_fields
			)
		
		# Add the files to upload
		parts.extend(
			[ part_boundary,
			  'Content-Disposition: file; name="%s"; filename="%s"' % \
				 (field_name, filename),
			  'Content-Type: %s' % content_type,
			  '',
			  body,
			]
			for field_name, filename, content_type, body in self.files
			)
		
		# Flatten the list and add closing boundary marker,
		# then return CR+LF separated data
		flattened = list(itertools.chain(*parts))
		flattened.append('--' + self.boundary + '--')
		flattened.append('')
		return '\r\n'.join(flattened)

def FaceDetect(img_binary,img_name):
	"""detect face"""
	url = "%s/detection/detect?mode=oneface&api_secret=%s&api_key=%s" % (FACEPP_SERVER,API_SECRET,API_KEY)
	form = _MultiPartForm()
	form.add_file('img',img_name,img_binary)
	body = str(form)
	headers = {"Content-type":form.get_content_type(),'Content-length':str(len(body))}
	http_request = tornado.httpclient.HTTPRequest(url=url,method='POST',headers=headers,body=body)
	return http_request

def FaceCompare(face_id1,face_id2):
	""" compare face """
	url = "%s/recognition/compare?api_secret=%s&api_key=%s&face_id1=%s&face_id2=%s" % (FACEPP_SERVER,API_SECRET,API_KEY,face_id1,face_id2)
	http_request = tornado.httpclient.HTTPRequest(url=url)
	return http_request

def AddFace(person_name,face_id):
	""" compare face """
	url = "%s/person/add_face?api_secret=%s&api_key=%s&face_id=%s&person_name=%s" % (FACEPP_SERVER,API_SECRET,API_KEY,face_id,person_name)
	http_request = tornado.httpclient.HTTPRequest(url=url)
	return http_request

def CreatePerson(person_name,group_name = u'Students'):
	""" create person """
	url = "%s/person/create?api_secret=%s&api_key=%s&person_name=%s&group_name=%s" % (FACEPP_SERVER,API_SECRET,API_KEY,person_name,group_name)
	return url
