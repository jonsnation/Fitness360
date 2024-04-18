from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify,flash
from App.models import db, User, Workout, Routine
from App.controllers import create_user


index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def login_page():
    return render_template('login.html')
    

@index_views.route('/app', methods=['GET'])
def index_page():
    workouts = Workout.query.all()
    workout_id = 1  # replace with a valid workout ID
    workout = Workout.query.get(workout_id)
    flash('Login Successful')
    return render_template('index.html')


@index_views.route('/init', methods=['GET'])
def init():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass')
    return jsonify(message='db initialized!')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})