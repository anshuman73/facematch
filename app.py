from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
import face_match


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:No1cancrackthis@localhost:5432/facematch'
app.config['UPLOAD_FOLDER'] = '/uploads'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'this_is_a_secret_key'

db = SQLAlchemy(app)
admin = Admin(app, name='FaceMatch', template_mode='bootstrap3')


from views import *
from models import *
from admin import *

db.create_all()


if __name__ == '__main__':
    app.run()
