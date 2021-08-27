from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Artist
from forms import UserForm, ArtistForm
from sqlalchemy.exc import IntegrityError

import requests

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresl:///simply_art"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


res = requests.get(
    'https://api.unsplash.com/photos/random?client_id=sjb8Hy9YhaHInjGNWAwQM9DMQdh4niqP7hiHnTlpGkU')

data = res.json()

connect_db(app)

toolbar = DebugToolbarExtension(app)


@app.route('/')
def home_page():
    return render_template('index.html')


@app.route('/messages', methods=['GET', 'POST'])
def show_messages():
    if "user_id" not in session:
        flash("Please login first!", "danger")
        return redirect('/')
    form = ArtistForm()
    all_messages = message.query.all()
    if form.validate_on_submit():
        text = form.text.data
        new_message = Message(text=text, user_id=session['user_id'])
        db.session.add(new_message)
        db.session.commit()
        flash('Tweet Created!', 'success')
        return redirect('/messages')

    return render_template("messages.html", form=form, messages=all_messages)


@app.route('/messages/<int:id>', methods=["POST"])
def delete_tweet(id):
    """Delete message"""
    if 'user_id' not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    message = message.query.get_or_404(id)
    if message.user_id == session['user_id']:
        db.session.delete(message)
        db.session.commit()
        flash("Tweet deleted!", "info")
        return redirect('/messages')
    flash("You don't have permission to do that!", "danger")
    return redirect('/messages')


@app.route('/register', methods=['GET', 'POST'])
def register_user():
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        new_user = User.register(username, password)

        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username taken.  Please pick another')
            return render_template('register.html', form=form)
        session['user_id'] = new_user.id
        flash('Welcome! Successfully Created Your Account!', "success")
        return redirect('/messages')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            flash(f"Welcome Back, {user.username}!", "primary")
            session['user_id'] = user.id
            return redirect('/messages')
        else:
            form.username.errors = ['Invalid username/password.']

    return render_template('login.html', form=form)


@app.route('/logout')
def logout_user():
    session.pop('user_id')
    flash("Goodbye!", "info")
    return redirect('/')
