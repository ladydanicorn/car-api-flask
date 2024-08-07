from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.models import Car
from app import db
from . import bp

@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_car():
    if request.method == 'POST':
        new_car = Car(
            make=request.form['make'],
            model=request.form['model'],
            year=int(request.form['year']),
            description=request.form['description'],
            user_id=current_user.id
        )
        db.session.add(new_car)
        db.session.commit()
        flash('Your car has been added!')
        return redirect(url_for('auth.profile'))
    return render_template('cars/add_car.html')

@bp.route('/')
def index():
    cars = Car.query.all()
    return render_template('cars/index.html', cars=cars)

@bp.route('/<uuid:car_id>')
def get_single_car(car_id):
    car = Car.query.get_or_404(car_id)
    return render_template('cars/single_car.html', car=car)

@bp.route('/edit/<uuid:car_id>', methods=['GET', 'POST'])
@login_required
def edit_car(car_id):
    car = Car.query.get_or_404(car_id)
    if car.owner != current_user:
        flash('You can only edit your own cars.')
        return redirect(url_for('auth.profile'))
    if request.method == 'POST':
        car.make = request.form['make']
        car.model = request.form['model']
        car.year = int(request.form['year'])
        car.description = request.form['description']
        db.session.commit()
        flash('Your car has been updated!')
        return redirect(url_for('auth.profile'))
    return render_template('cars/edit_car.html', car=car)

@bp.route('/delete/<uuid:car_id>')
@login_required
def delete_car(car_id):
    car = Car.query.get_or_404(car_id)
    if car.owner != current_user:
        flash('You can only delete your own cars.')
        return redirect(url_for('auth.profile'))
    db.session.delete(car)
    db.session.commit()
    flash('Your car has been deleted!')
    return redirect(url_for('auth.profile'))