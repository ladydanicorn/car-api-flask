from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import User, Car
from app import db
from werkzeug.security import check_password_hash
import uuid
from functools import wraps

bp = Blueprint('api', __name__)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('X-API-Token')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        user = User.query.filter_by(api_token=token).first()
        if not user:
            return jsonify({'message': 'Token is invalid!'}), 401
        
        return f(user, *args, **kwargs)
    return decorated

@bp.route('/login', methods=['POST'])
def api_login():
    data = request.json
    user = User.query.filter_by(username=data.get('username')).first()
    if user and check_password_hash(user.password, data.get('password')):
        return jsonify({'token': user.api_token})
    return jsonify({'message': 'Invalid credentials'}), 401

@bp.route('/cars', methods=['GET'])
@token_required
def get_cars(current_user):
    cars = Car.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        'id': car.id,
        'make': car.make,
        'model': car.model,
        'year': car.year,
        'description': car.description
    } for car in cars])

@bp.route('/cars', methods=['POST'])
@token_required
def create_car(current_user):
    data = request.json
    new_car = Car(
        make=data['make'],
        model=data['model'],
        year=data['year'],
        description=data.get('description', ''),
        user_id=current_user.id
    )
    db.session.add(new_car)
    db.session.commit()
    return jsonify({
        'id': new_car.id,
        'make': new_car.make,
        'model': new_car.model,
        'year': new_car.year,
        'description': new_car.description
    }), 201

@bp.route('/cars/<string:car_id>', methods=['GET'])
@token_required
def get_car(current_user, car_id):
    car = Car.query.filter_by(id=car_id, user_id=current_user.id).first()
    if not car:
        return jsonify({'message': 'Car not found'}), 404
    return jsonify({
        'id': car.id,
        'make': car.make,
        'model': car.model,
        'year': car.year,
        'description': car.description
    })

@bp.route('/cars/<string:car_id>', methods=['PUT'])
@token_required
def update_car(current_user, car_id):
    car = Car.query.filter_by(id=car_id, user_id=current_user.id).first()
    if not car:
        return jsonify({'message': 'Car not found'}), 404
    
    data = request.json
    car.make = data.get('make', car.make)
    car.model = data.get('model', car.model)
    car.year = data.get('year', car.year)
    car.description = data.get('description', car.description)
    
    db.session.commit()
    return jsonify({
        'id': car.id,
        'make': car.make,
        'model': car.model,
        'year': car.year,
        'description': car.description
    })

@bp.route('/cars/<string:car_id>', methods=['DELETE'])
@token_required
def delete_car(current_user, car_id):
    car = Car.query.filter_by(id=car_id, user_id=current_user.id).first()
    if not car:
        return jsonify({'message': 'Car not found'}), 404
    
    db.session.delete(car)
    db.session.commit()
    return jsonify({'message': 'Car deleted successfully'})