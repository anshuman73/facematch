from PIL import Image
import face_recognition
import os

for file in os.listdir():
	if not file.endswith('.py'):
		image = face_recognition.load_image_file(file)
		face_locations = face_recognition.face_locations(image)
		print("I found {} face(s) in this photograph.".format(len(face_locations)))
		
		for index, face_location in enumerate(face_locations):
		    top, right, bottom, left = face_location
		    print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))
		    face_image = image[top:bottom, left:right]
		    pil_image = Image.fromarray(face_image)
		    pil_image.save(file.split('-')[-1].split('.')[0] + '.jpg')