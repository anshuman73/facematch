import face_recognition
from PIL import Image
import numpy as np
import os

known_faces = []
known_faces_names = []

working_dir = os.getcwd() + '/' + 'Faces'

for file in os.listdir(working_dir):
    known_faces.append((face_recognition.face_encodings(face_recognition.load_image_file(working_dir + '/' + file))[0]))
    known_faces_names.append(file.rsplit('.', 1)[0])


def give_match(file_path):
    unknown_faces = face_recognition.face_encodings(face_recognition.load_image_file(file_path))
    people_found = []
    print(known_faces_names)
    for face in unknown_faces:
        face_distances = face_recognition.face_distance(known_faces, face)
        face_distances = ['{0:.2f}'.format((1-x) * 100) for x in face_distances]
        print(face_distances)
        max_index = face_distances.index(max(face_distances))
        max_match_person = known_faces_names[max_index]
        people_found.append(max_match_person)

    return people_found
