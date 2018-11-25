from app import db


class User(object):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.UnicodeText, unique=True)
    full_name = db.Column(db.UnicodeText)


class Teacher(db.Model, User):
    courses_taught = db.relationship('Course', backref='teacher', lazy=True)


courses = db.Table('courses',
                   db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True),
                   db.Column('student_id', db.Integer, db.ForeignKey('student.id'), primary_key=True)
                   )


class Student(db.Model, User):
    courses_taken = db.relationship('Course', secondary=courses, lazy='subquery',
                                    backref=db.backref('students', lazy=True))
    attendance = db.relationship('Attendance', backref='student', lazy=True)


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.UnicodeText)
    course_teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
    classes = db.relationship('Class', backref='course', lazy=True)


class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    date = db.Column(db.Date)
    attendance = db.relationship('Attendance', backref='class', lazy=True)


class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    attended = db.Column(db.Boolean, default=False)

    def __init__(self, course_id, class_id, student_id, attended=True):
        self.class_id = class_id
        self.course_id = course_id
        self.student_id = student_id
        self.attended = attended
