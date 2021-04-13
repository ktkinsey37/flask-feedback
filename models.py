"""Models for Feedback project"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, BooleanField, SelectField
from wtforms.fields.html5 import URLField
from wtforms.validators import Length, URL, Optional, NumberRange