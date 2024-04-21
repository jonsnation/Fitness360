from App.models import Routine
from App.database import db


def create_routine(name, description, user_id):
    routine = Routine(name=name, description=description, user_id=user_id)
    db.session.add(routine)
    db.session.commit()
    return routine

def get_all_routines():
    return Routine.query.all()

def get_routine(id):
    return Routine.query.get(id)

def get_user_routines(user_id):
    return Routine.query.filter_by(user_id=user_id).all()

def get_all_routines_json():
    routines = get_all_routines()

    if not routines:
        return[]

    return [routine.get_json() for routine in routines]

def update_routine(id, name=None):
    routine = Routine.query.get(id)
    if name is not None:
        routine.name = name
    db.session.commit()
    return routine


def delete_routine(id):
    routine = Routine.query.filter_by(routine_id=id).first()
    workouts = get_all_workouts_in_routines(id)
    if routine:
        db.session.delete(routine)
        for workout in workouts: 
            db.session.delete(workout)
        db.session.commit()
        return routine
    else:
        return None
