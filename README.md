# FaceMatch

A Facial Recognition based Attendance System made for academic institutions.

The software can clean your face data, and store the different faces in the database.

On uploading an image of the class, it automatically picks up the faces of the students prensent, and compares them with the faces in the database, and marks attendance for those found.

Accuracy acheieved in tests - 94%


## Instructions

Create two directories - /uploads and /faces. Save all processed, cleaned faces in the /faces directly.
Can use the face_recognition library used for cleaning of the facial data.

Simply run the app.py file by using ```python3 app.py``` (Python2 not supported, preferred version is CPython 3.6.7)
