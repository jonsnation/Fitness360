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
@index_views.route('/app/<routine_id>', methods=['GET'])
@jwt_required()
def index_page(workout_id = 1):
    workouts = get_all_workouts()
    routine = create_routine("back day", 1)
    add_selected_workout_to_routine(routine, 5)
    add_selected_workout_to_routine(routine, 6)
    add_selected_workout_to_routine(routine, 1)
    routines = get_user_routines(1)
    declared_routine = get_routine_by_id(routine_id)
    
    

    if workout_id is not None:
        selected_workout = Workout.query.get(workout_id)
    else:
        selected_workout = None

    return render_template('index.html', workouts=workouts, routines=routines, workout_routines=workout_routines, selected_workout=selected_workout, selected_routine=selected_routine, current_user=jwt_current_user)

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
    # workouts = Workout.query.all()
    # for workout in workouts:
    #     print(workout.get_json())
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
    try:
        data = request.form
        routine_name = data["name"]
        routine = create_routine(current_user.id, routine_name)
        if  routine == create_routine(current_user.id, routine_name):
            routine_workouts = request.form.getlist('selected_workouts[]')
            for workout_id in routine_workouts:
                add_selected_workout_to_routine(routine, workout_id)
            flash('New routine created!')
        else: 
            flash('Error creating routine')
    except Exception as e:
        flash(f'Error creating routine: {str(e)}', 'error')
    return redirect(url_for('index_views.index_page'))



# # View/Edit routine
# @routine_views.route('/routine/edit/<int:id>', methods=['GET', 'POST'])
# @jwt_required
# def edit_routine2(id):
#     routine = get_routine(id)
#     if not routine or routine.user_id != jwt_current_user.id:
#         return redirect(url_for('user_views.display_routines'))

#     if request.method == 'POST':
#         name = request.form.get('name')
#         description = request.form.get('description')
#         updated_routine = update_routine(id, name=name, description=description)
#         if updated_routine:
#             return redirect(url_for('user_views.display_routines'))

#     workouts = get_all_workouts()
#     return render_template('routine_form.html', form_action=url_for('user_views.edit_routine2', id=id), routine=routine, workouts=workouts)

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