from App.models import User, Routine, Workout, WorkoutRoutine
from App.database import db

def create_user(username, password):
    newuser = User(username=username, password=password)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_user(id):
    return User.query.get(id)

def get_all_users():
    return User.query.all()

def get_all_users_json():
    users = User.query.all()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        db.session.add(user)
        return db.session.commit()
    return None

def create_routine_declaration(self):
    declaration = Routine(self.id, 'Basic Routine')
    db.session.add(declaration)
    db.session.commit()
    return declaration  

def create_routine(self, name):
    routine = Routine(user_id = self.id, name=name)
    db.session.add(routine)
    db.session.commit()
    return routine

def find_routine(self, name):
    find = Routine.query.filter_by(user_id=self.id, name=name).first()
    if find:
        return find
    else:
        return None
    return None
    
def find_workout (self, routine_id, workout_id):
    find = WorkoutRoutine.query.filter_by(user_id = self.id, workout_id = workout_id, routine_id = routine_id).first()
    if find:
        return False
    else:
        return True

def add_workout_to_routine(self, routine_id, workout_id):
    workout_routine = WorkoutRoutine(self.id, routine_id=routine_id, workout_id=workout_id)
    db.session.add(workout_routine)
    db.session.commit()
    return workout_routine

#check
def remove_workout_from_routine(self, routine_id, workout_id):
    workout_routine =WorkoutRoutine.query.filter_by(user_id=self.id, routine_id=routine_id, workout_id=workout_id)
    db.session.commit()
    return None