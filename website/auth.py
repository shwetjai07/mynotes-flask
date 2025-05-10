from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login',  methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if user.password and check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', category='success')
    return redirect(url_for('auth.login'))

@auth.route('/signup',  methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        # Handle sign-up logic here
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        email = request.form.get('email')

        if len(username) <= 2:
            flash('Username must be greater than 2 characters.', category='error')
        elif len(password1) < 8:
            flash('Password must be at least 8 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error')
        else:
            # Check if user already exists
            user = User.query.filter_by(email=email).first()
            if user:
                flash('Email already exists.', category='error')
            else:
                # Add new user to the database
                hash_method = 'pbkdf2'  # Change this to 'pbkdf2:sha256', 'argon2', etc., if needed
                new_user = User(email=email, username=username, password=generate_password_hash(password1, method=hash_method))
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True)

                flash('Account created!', category='success')
                return redirect(url_for("views.home"))
            
    return render_template('sign_up.html', user=current_user)