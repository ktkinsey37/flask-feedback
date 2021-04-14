"""App routes for Feedback project"""

from flask import Flask, request, render_template, redirect, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, BooleanField
from wtforms.validators import Length, URL
from forms import CreateUserForm, LoginForm, CreateFeedbackForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'password'  

connect_db(app)
db.create_all()

@app.route('/')
def homepage():
    return redirect('/register', code=302)

@app.route('/register', methods=["GET", "POST"])
def registration_form():
    """Show and handle user registration form"""

    form = CreateUserForm()

    if form.validate_on_submit():
        current_user = User.register(form.username.data, form.password.data, form.email.data, form.first_name.data, form.last_name.data)
        db.session.add(current_user)
        db.session.commit()
        session["username"] = current_user.username
        return redirect(f'/users/{current_user.username}', code=302)

    else:
        return render_template('register_form.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login_form():
    """Show and handle user login form"""

    form = LoginForm()

    if form.validate_on_submit():
        current_user = User.authenticate(form.username.data, form.password.data)
        if current_user:
            session["username"] = current_user.username
            return redirect(f'/users/{current_user.username}', code=302)
        else:
            flash(f"Your username and password did not match")
            return render_template('login_form.html', form=form)
    return render_template('login_form.html', form=form)

@app.route('/users/<username>', methods=["GET"])
def user_page(username):
    if "username" not in session:
        flash("Please login first")
        return redirect('/login', code=302)
    else:
        user = User.query.filter_by(username=session['username']).first()
        feedback = Feedback.query.filter_by(username=user.username).all()
        return render_template('userpage.html', user=user, feedback=feedback)

@app.route('/logout')
def logout_user():
    session.pop('username')
    return redirect('/', code=302)

@app.route('/users/<username>/delete', methods=["POST"])
def delete_user(username):
    if "username" not in session:
        flash("Please login first")
        return redirect('/login', code=302)
    else:
        user = User.query.filter_by(username=session["username"]).first()
        feedbacks = Feedback.query.filter_by(username=username).all()
        db.session.delete(user)
        for feedback in feedbacks:
            db.session.delete(feedback)
        db.session.commit()
        session.pop('username')
        return redirect('/', code=302)

@app.route('/users/<username>/feedback/add', methods=["GET", "POST"])
def add_feedback_route(username):
    form = CreateFeedbackForm()
    if "username" not in session:
        flash("Please login first")
        return redirect('/login', code=302)
    elif form.validate_on_submit():
        feedback = Feedback(title=form.title.data, content=form.content.data, username=session['username'])
        db.session.add(feedback)
        db.session.commit()
        return redirect(f'/users/{session["username"]}', code=302)
    else:
        return render_template('add_feedback.html', form=form)

@app.route('/feedback/<int:feedback_id>/update', methods=["GET", "POST"])
def edit_feedback(feedback_id):
    form = CreateFeedbackForm()
    if "username" not in session:
        flash("Please login first")
        return redirect('/login', code=302)
    username = session["username"]
    feedback = Feedback.query.filter_by(id=feedback_id).first()
    if feedback.username != username:
        flash("That feedback can only be edited by the user that created it")
        return redirect('/login', code=302)
    elif form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.commit()
        return redirect(f'/users/{username}', code=302)
    else:
        return render_template('add_feedback.html', form=form)

@app.route('/feedback/<int:feedback_id>/delete', methods=["POST"])
def delete_feedback(feedback_id):
    if "username" not in session:
        flash("Please login first")
        return redirect('/login', code=302)
    username = session["username"]
    feedback = Feedback.query.filter_by(id=feedback_id).first()
    if feedback.username != username:
        flash("That feedback can only be deleted by the user that created it")
        return redirect('/login', code=302)
    else:
        db.session.delete(feedback)
        db.session.commit()
        return redirect(f'/users/{username}', code=302)
