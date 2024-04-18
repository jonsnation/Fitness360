from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from App.models import User, Workout, Routine

from.index import index_views

from App.controllers import (
    create_user,
    get_all_users,
    get_all_users_json,
    jwt_required,
    create_routine,
    get_all_routines,
    get_routine,
    get_user_routines,
    update_routine,
    add_workout_to_routine,
    delete_routine
)

routine_views = Blueprint('routine_views', __name__, template_folder='../templates')

# Create routines
@routine_views.route('/routine/create', methods=['POST'])
@jwt_required
def create_routine2():
    data = request.json
    routine = create_routine(data['name'], data['description'], jwt_current_user.id)
    return jsonify(routine.get_json())

# Add workout to routine
@routine_views.route('/routine/<int:routine_id>/add_workout', methods=['POST'])
@jwt_required
def add_workout(routine_id):
    workout_id = request.form.get('workout_id')
    add_workout_to_routine(routine_id, workout_id)
    return redirect(url_for('user_views.edit_routine2', id=routine_id))

# View/Edit routine
@routine_views.route('/routine/edit/<int:id>', methods=['GET', 'POST'])
@jwt_required
def edit_routine2(id):
    routine = get_routine(id)
    if not routine or routine.user_id != jwt_current_user.id:
        return redirect(url_for('user_views.display_routines'))

    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        updated_routine = update_routine(id, name=name, description=description)
        if updated_routine:
            return redirect(url_for('user_views.display_routines'))

    workouts = get_all_workouts()
    return render_template('routine_form.html', form_action=url_for('user_views.edit_routine2', id=id), routine=routine, workouts=workouts)

# Delete routine
@routine_views.route('/routine/delete/<int:id>', methods=['POST'])
@jwt_required
def delete_routine2(id):
    routine = get_routine(id)
    if not routine or routine.user_id != jwt_current_user.id:
        return redirect(url_for('user_views.display_routines'))

    deleted_routine = delete_routine(id)
    if deleted_routine:
        return redirect(url_for('user_views.display_routines'))

    return 'Failed to delete routine', 400