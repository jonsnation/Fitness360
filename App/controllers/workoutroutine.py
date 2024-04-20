from App.models import WorkoutRoutine
from App.database import db

def get_all_workout_routines():
    val = WorkoutRoutine.query.all()
    print(val)
    return 

def get_workout_routines_json():
    workout_routines = get_all_workout_routines()

    if not workout_routines:
        return[]

    return[workout_routines.get_json() for workout_routine in workout_routines]

def get_all_workouts_in_routines(routine_id):
    return WorkoutRoutine.query.filter_by(routine_id=routine_id)