from facepp import API , File

# facepp key
API_KEY = 'b3b9061aaf64ea2515a3538dfb624e94'
API_SECRET = 'OfvW6DdyM9iqAa8TkBoBhoiWANX6Kn2Z'

api = API(API_KEY, API_SECRET)


"""
Get the face id
"""
def DetectFace(filepath):

	face_detect = api.detection.detect(img = File(filepath))

	if face_detect['face'] != []:
		return face_detect['face'][0]['face_id']
	else:
		return -1;

def CompareFace(face_id1 , face_id2):

	face_compare = api.recognition.compare(face_id1 = face_id1 , face_id2 = face_id2)

	if face_compare.has_key("similarity"):
		return face_compare["similarity"]
	else:
		return -1

if __name__ == '__main__':
	face1 = DetectFace("img/1130339074145420272757.jpg")
	face2 = DetectFace("img/5100309150103924400835.jpg")
	print face1 , face2

	cmp_result = CompareFace(face1 , face2)

	print cmp_result
