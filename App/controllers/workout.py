from App.models import Workout
from App.database import db

def get_all_workouts():
    return Workout.query.all()

def get_workout_by_id(id):
    return workout.query.filter_by(id=id).first()

def get_workout_by_name(name):
    return Workout.query.filter_by(name=name).first()