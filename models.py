"""Models for Feedback project"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, BooleanField, SelectField
from wtforms.fields.html5 import URLField
from wtforms.validators import Length, URL, Optional, NumberRange
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    def __repr__(self):
        u = self
        return f'<User {u.username} {u.email} {u.first_name} {u.last_name}>'

    __tablename__ = 'users'

    username = db.Column(db.String(20),
                    primary_key=True,
                    unique=True)

    password = db.Column(db.String,
                    nullable=False)

    email = db.Column(db.String(50), nullable=False)

    first_name = db.Column(db.String(30), nullable=False)

    last_name = db.Column(db.String(30), nullable=False)

    feedback = db.relationship('Feedback', backref="user")

    def serialize_user(self):
        return {
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.imaglast_name}

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Register user with a hashed password and return the user"""

        hashed = bcrypt.generate_password_hash(password)

        hashed_utf8 = hashed.decode("utf8")

        return cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)

    @classmethod
    def authenticate(cls, username, password):

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, password):
            return u
        else:
            return False

class Feedback(db.Model):
    def __repr__(self):
        f = self
        return f'<Feedback {f.id} {f.title} {f.username}>'

    __tablename__ = 'feedback'

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)

    title = db.Column(db.String(100),
                    nullable=False)

    content = db.Column(db.String,
                        nullable=False)

    username = db.Column(db.String,
                        db.ForeignKey('users.username'))