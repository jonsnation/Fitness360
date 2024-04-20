from App.models import Routine
from App.database import db


# def create_routine2(name, description, user_id):
#     routine = Routine(name=name, description=description, user_id=user_id)
#     db.session.add(routine)
#     db.session.commit()
#     return routine

def get_all_routines():
    return Routine.query.all()
    
def get_routine_by_name(name):
    return Routine.query.filter_by(name=name).first()

def get_routine_by_id(id):
    routine = Routine.query.filter_by(routine_id=id).first()
    return routine

def get_user_routines(user_id):
    return Routine.query.filter_by(user_id=user_id).all()

def get_all_routines_json():
    routines = get_all_routines()

    if not routines:
        return[]

    return [routine.get_json() for routine in routines]

def update_routine(id, name=None, description=None):
    routine = Routine.query.get(id)
    if name is not None:
        routine.name = name
    if description is not None:
        routine.description = description
    db.session.commit()
    return routine

# def add_workout_to_routine(self, workout_id, routine_id):
#     # routine = Routine.query.get(routine_id)
#     try:
#         workout = WorkoutRoutine(workout_id=workout_id, routine_id=routine_id)
#         db.session.add(workout)
#         db.session.commit()
#         return workout
#     except Exception as e:
#         print(e)
#         db.session.rollback()
#         return None

def delete_routine(id):
    routine = Routine.query.get(id)
    db.session.delete(routine)
    db.session.commit()
