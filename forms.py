from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length


class LoginForm(FlaskForm):
    username = StringField('User Name', validators=[InputRequired('Username is a required field'),
                                                   Length(min=4, max=32, message='Username must be 4-32 characters')])
    password = PasswordField('Password', validators=[InputRequired('Password is a required field')])
