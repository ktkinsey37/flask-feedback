"""Forms for Feedback project"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, BooleanField, SelectField, PasswordField
from wtforms.fields.html5 import URLField, EmailField
from wtforms.validators import Length, URL, Optional, NumberRange, Email, email_validator

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class CreateUserForm(FlaskForm):
    """Form for adding users"""

    username = StringField("Username", validators=[Length(1,20)])
    password  = PasswordField('Password')
    email = StringField("Valid email address", validators=[Email(), Length(1,50)])
    first_name = StringField("First name", validators=[Length(1,30)])
    last_name = StringField("Last name", validators=[Length(1,30)])

class LoginForm(FlaskForm):
    """Login form for users"""

    username = StringField("Username", validators=[Length(1,20)])
    password  = PasswordField('Password')

class CreateFeedbackForm(FlaskForm):
    """Form for creating feedback"""

    title = StringField("Title", validators=[Length(1,100)])
    content = StringField("Content of feedback")