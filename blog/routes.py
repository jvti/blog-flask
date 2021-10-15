
import hashlib
import secrets
# from PIL import Image
from flask.globals import request
from flask.helpers import flash
from wtforms.validators import Email
from blog import app, db, bcrypt, images
from blog.forms import RegistratoinForm, LoginForm
from flask import render_template, redirect, url_for
from blog.models import User
from flask_login import login_user


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistratoinForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        filename = images.save(form.image.data, name=hashlib.md5(form.username.data.encode('utf-8')).hexdigest() + ".")
        user = User(name=form.name.data, avatar=filename, username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Registered Successfully!',category="info")
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username= form.username.data).first()
        print(user)
        if user and bcrypt.check_password_hash(form.password, form.password.data):
            login_user(user, remember= form.remember.data)
            flash('Logged in Successfully!', category="info")
            return redirect(url_for('index'))

        else:
            flash('Usernae or Password is not Correct!' , category='primary')    
    return render_template('login.html', form=form)



@app.route('/logout')
def logout():
    pass