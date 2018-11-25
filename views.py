from app import app, db
from flask import session, redirect, url_for, render_template, abort, request, flash
from forms import LoginForm
from models import Student, Teacher, Course, Class, Attendance
import os
from werkzeug.utils import secure_filename
from face_match import give_match


ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']


@app.route('/index', methods=['GET'])
@app.route('/', methods=['GET'])
def index():
    if session.get('logged_in') and session.get('username'):
        if session.get('role') == 'teacher':
            return redirect(url_for('teacher_dashboard'))
        elif session.get('role') == 'student':
            return redirect((url_for('student_dashboard')))
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET'])
def login():
    if session.get('logged_in') and session.get('username'):
        return redirect(url_for('dashboard'))
    else:
        return render_template('main_login.html')


@app.route('/login/<role>', methods=['GET', 'POST'])
def login_role(role):
    form = LoginForm()
    if form.validate_on_submit():
        username, password = form.username.data, form.password.data
        # TODO: Actually verify password
        if role == 'student':
            student = Student.query.filter_by(username=username).first()
            if student:
                session['logged_in'] = True
                session['username'] = username
                session['role'] = 'student'
                return redirect(url_for('student_dashboard'))
            else:
                form.username.errors.append('Unknown username')
                return render_template('student_login.html', form=form)
        elif role == 'teacher':
            teacher = Teacher.query.filter_by(username=username).first()
            if teacher:
                session['logged_in'] = True
                session['username'] = username
                session['role'] = 'teacher'
                return redirect(url_for('teacher_dashboard'))
            else:
                form.username.errors.append('Unknown username')
                return render_template('teacher_login.html', form=form)
        else:
            return abort(403)
    else:
        if role == 'student':
            return render_template('student_login.html', form=form)
        elif role == 'teacher':
            return render_template('teacher_login.html', form=form)
        else:
            return abort(404)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/teacher', methods=['GET'])
def teacher_dashboard():
    if session.get('role') == 'teacher':
        username = session.get('username')
        teacher = Teacher.query.filter_by(username=username).first()
        courses = teacher.courses_taught
        return render_template('teacher_dashboard.html', courses=courses)
    else:
        return abort(403)


@app.route('/teacher/course/<course_name>', methods=['GET', 'POST'])
def get_course(course_name):
    if session.get('role') == 'teacher':
        username = session.get('username')
        teacher = Teacher.query.filter_by(username=username).first()
        course = Course.query.filter_by(teacher=teacher).filter_by(course_name=course_name).first()
        if course:
            classes = course.classes
            return render_template('course_timings.html', course=course, classes=classes)
        else:
            return abort(403)
    else:
        return abort(403)


@app.route('/teacher/course/<course_name>/<class_date>', methods=['GET', 'POST'])
def get_class(course_name, class_date):
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(os.getcwd() + '/' + app.config['UPLOAD_FOLDER'], filename))
            people_found = give_match(os.path.join(os.getcwd() + '/' + app.config['UPLOAD_FOLDER'], filename))
            username = session.get('username')
            teacher = Teacher.query.filter_by(username=username).first()
            course = Course.query.filter_by(teacher=teacher).filter_by(course_name=course_name).first()
            the_class = Class.query.filter_by(course=course).filter_by(date=class_date).first()
            for people in people_found:
                people = people.strip()
                print(people)
                student = Student.query.filter_by(full_name=people).first()
                if student:
                    attendance = Attendance(course.id, the_class.id, student.id, True)
                    db.session.add(attendance)
                    db.session.commit()
                else:
                    print('Student not detected')
            return redirect(request.url)
    else:
        if session.get('role') == 'teacher':
            username = session.get('username')
            teacher = Teacher.query.filter_by(username=username).first()
            course = Course.query.filter_by(teacher=teacher).filter_by(course_name=course_name).first()
            if course:
                the_class = Class.query.filter_by(course=course).filter_by(date=class_date).first()
                attendance = the_class.attendance
                return render_template('class.html', course=course, the_class=the_class, attendances=attendance)
            else:
                return abort(403)
        else:
            return abort(403)
