from app import admin, db
from flask_admin.contrib.sqla import ModelView
from models import Student, Teacher, Course, Class, Attendance

admin.add_view(ModelView(Student, db.session))
admin.add_view(ModelView(Teacher, db.session))
admin.add_view(ModelView(Course, db.session))
admin.add_view(ModelView(Class, db.session))
admin.add_view(ModelView(Attendance, db.session))
