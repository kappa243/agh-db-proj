import datetime

import sqlalchemy
from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_login import login_user, login_required, current_user, logout_user

from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST', 'GET'])
def login_post():
    if request.method == "POST":
        if 'login_data' in request.form:
            username = request.form['username']
            password = request.form['password']

            user = db.session.query(User).filter_by(username=username).with_for_update().first()

            if not user or not check_password_hash(user.password, password):
                flash('Please check your login details and try again.')
                return render_template('login.html')
            user.last_login = datetime.datetime.utcnow()
            db.session.commit()
            login_user(user)
            return redirect(url_for('index'))

    return render_template('login.html')


@auth.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == "POST":
        if 'register_data' in request.form:
            username = request.form['username']
            password1 = request.form['password1']
            password2 = request.form['password2']
            user = User.query.filter_by(username=username).first()
            if user:
                flash('User with this name already exists')
                # return render_template('register.html')
            elif len(username) < 1:
                flash('Username must minimum 1 character long')
            elif password1 != password2:
                flash('Passwords differentiate')
            elif len(password1) < 3:
                flash('Password must be minimum 3 characters long')
            else:
                newUser = User(username=username, password=generate_password_hash(password1, method='sha256'),
                               registration_date=datetime.datetime.utcnow(), admin=False)
                db.session.add(newUser)
                db.session.commit()
                print(username, password1, password2)
                return redirect(url_for('auth.login_post'))

    return render_template('register.html')


@auth.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login')
