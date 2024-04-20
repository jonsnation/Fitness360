from App.models import WorkoutRoutine
from App.database import db

def get_all_workout_routines():
    return WorkoutRoutine.query.all()

def get_workout_routines_json():
    workout_routines = get_all_workout_routines()

    if not workout_routines:
        return[]

    return[workout_routines.get_json() for workout_routine in workout_routines]

def add_selected_workouts_to_routine(routine, selected_exercises):
    for exercise_id in selected_exercises:
        workout_routine = WorkoutRoutine(routine_id=routine.routine_id, user_id=routine.user_id, workout_id=exercise_id)
        db.session.add(workout_routine)
    db.session.commit()

def get_all_workouts_in_routines(routine_id):
    return WorkoutRoutine.query.filter_by(routine_id=routine_id)