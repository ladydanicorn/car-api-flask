import uuid
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from app.models import Car
from app import db
from . import bp

@bp.route('/profile')
@login_required
def profile():
    user_cars = Car.query.filter_by(user_id=current_user.id).all()
    return render_template('auth/profile.html', user=current_user, cars=user_cars, api_token=current_user.api_token)

@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists')
            return redirect(url_for('auth.signup'))
        
        new_user = User(
            username=username,
            password=generate_password_hash(password),
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registered successfully! Please log in.')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/signup.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully.')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password')
    return render_template('auth/login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.')
    return redirect(url_for('home'))