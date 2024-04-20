from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify,flash, url_for
from App.models import db, User, Workout, Routine
from flask_jwt_extended import jwt_required, current_user as jwt_current_user, unset_jwt_cookies, set_access_cookies

import csv

from App.controllers import (
    create_user,
    get_user_by_username,
    get_user,
    get_all_users,
    get_all_users_json,
    jwt_required,
    create_routine,
    create_routine_declaration,
    find_routine,
    find_workout,
    get_all_routines,
    get_routine_by_name,
    get_routine_by_id,
    get_user_routines,
    update_routine,
    add_workout_to_routine,
    delete_routine,
    get_all_workout_routines,
    get_all_workouts_in_routines,
    get_all_workouts,
    get_workout_by_id,
    get_workout_by_name,
)


index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def login_page():
    return render_template('login.html')
    
# @index_views.route('/app', defaults={'workout_id': None}, methods=['GET'])
@index_views.route('/app', methods=['GET'])
@index_views.route('/app/<workout_id>', methods=['GET'])
@index_views.route('/app/routine/<routine_id>', methods=['GET'])
@index_views.route('/app/<workout_id>/<routine_id>', methods=['GET'])
@jwt_required()
def index_page(workout_id = 1, routine_id = 1):
    workouts = get_all_workouts()
    declared_routine = get_routine_by_id(routine_id)
    routines = get_user_routines(jwt_current_user.id)
    user_routines = get_all_workouts_in_routines(routine_id)

    if declared_routine:
        workout_routines = get_all_workout_routines()
        selected_routine = get_routine_by_id(declared_routine.routine_id)
        
    else:
        declared_routine = create_routine_declaration(jwt_current_user)
        workout_routines = get_all_workout_routines()
        selected_routine = get_routine_by_id(declared_routine.routine_id)
        user_routines = get_all_workouts_in_routines(declared_routine.routine_id)

    if workout_id is not None:
        selected_workout = Workout.query.get(workout_id)
    else:
        selected_workout = None
    
    print("here for workout routine:")
    print(workout_routines)
    print("?")
    return render_template('index.html', workouts=workouts, routines=routines, workout_routines=workout_routines, selected_workout=selected_workout, selected_routine=selected_routine, current_user=jwt_current_user, user_routines=user_routines)

@index_views.route('/app/view/<routine_id>')
@jwt_required()
def view_routine_page(routine_id):
    selected_routine= get_routine_by_id(routine_id)

    if selected_routine is None:
        flash('Routine not valid.')
        return redirect(url_for('index_views.index_page'))
    flash('Here is your routine.')
    return render_template('index_views.index_page', selected_routine=selected_routine)

    
@index_views.route('/init', methods=['GET'])
def initialize():
    db.drop_all()
    db.create_all()
    null_found = False
    # Load workouts from CSV file
    with open('workout.csv', encoding='unicode_escape') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(row)
            # Check for null values in the row
            if not all(row.values()):
                null_found = True
                continue
            workout = Workout(exercise_name=row['Exercise_Name'], 
                              exercise_image1=row['Exercise_Image'], 
                              exercise_image2=row['Exercise_Image1'], 
                              muscle_group=row['muscle_gp'], 
                              equipment=row['Equipment'], 
                              rating=float(row['Rating']), 
                              description=row['Description'])
            db.session.add(workout)
    db.session.commit()

    # # Print workouts to console
    if null_found:
        print("Null value(s) found and skipped")
    print("parsed csv successfully")
    create_user('bob', 'bobpass')
    print('database intialized')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})

# Action Routes


# Create routines
@index_views.route('/app/create', methods=['POST'])
@jwt_required()
def create_routine_route():
    data = request.form
    search_routine = find_routine(jwt_current_user, data['routine_name'])# not essential but up to y'all
    if not search_routine:
        routine = create_routine(jwt_current_user, data['routine_name'])
        flash('new routine made \(￣︶￣*\))')
        return  redirect(url_for('index_views.index_page'))
    else:
        flash("Could not make routine as it already exist")
        return  redirect(url_for('index_views.index_page'))

# Add workout to routine
@index_views.route('/addworkout/<int:routine_id>/<int:workout_id>', methods=['GET'])
@jwt_required()
def add_workout(routine_id, workout_id):
    routine_exercise = find_workout(jwt_current_user, routine_id=routine_id, workout_id=workout_id)

    if routine_exercise:
        add_workout_to_routine(jwt_current_user, routine_id=routine_id, workout_id=workout_id)
        flash('Workout added')
        return  redirect(url_for('index_views.index_page'))
    else:
        flash('Workout not added')
        return  redirect(url_for('index_views.index_page'))


# # Delete routine
# @routine_views.route('/routine/delete/<int:id>', methods=['POST'])
# @jwt_required
# def delete_routine2(id):
#     routine = get_routine(id)
#     if not routine or routine.user_id != jwt_current_user.id:
#         return redirect(url_for('user_views.display_routines'))

#     deleted_routine = delete_routine(id)
#     if deleted_routine:
#         return redirect(url_for('user_views.display_routines'))

#     return 'Failed to delete routine', 400