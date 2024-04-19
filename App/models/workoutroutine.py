from App.database import db

class WorkoutRoutine(db.Model):
    id = db.Column(db.Integer, primarykey = True)
    routine_id = db.Column(db.Integer,  db.ForeignKey('routine.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    workout_id = db.Column(db.Integer, db.ForeignKey('workout.workout_id'), nullable=False)

    def __init__(self, user_id, workout_id, routine_id):
        self.user_id = user_id
        self.workout_id = workout_id
        self.routine_id = routine_id
    
    def get_json(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "workout_id": self.workout_id,
            "routine_id": self.routine_id
        }