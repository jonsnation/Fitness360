from App.database import db
from math import floor

class Workout(db.Model):
    workout_id = db.Column(db.Integer, primary_key=True)
    exercise_name = db.Column(db.String, nullable=False)
    exercise_image1 = db.Column(db.String, nullable=True)
    exercise_image2 = db.Column(db.String, nullable=True)
    muscle_group = db.Column(db.String, nullable=False)
    equipment = db.Column(db.String, nullable=True)
    rating = db.Column(db.Float, nullable=True)
    description = db.Column(db.String, nullable=True)

    def __init__(self, exercise_name, exercise_image1, exercise_image2, muscle_group, equipment, rating, description):
        self.exercise_name = exercise_name
        self.exercise_image1 = exercise_image1
        self.exercise_image2 = exercise_image2
        self.muscle_group = muscle_group
        self.equipment = equipment
        self.rating = rating
        self.description = description

    def get_json(self):
        return {
            'workout_id': self.workout_id,
            'exercise_name': self.exercise_name,
            'exercise_image1': self.exercise_image1,
            'exercise_image2': self.exercise_image2,
            'muscle_group': self.muscle_group,
            'equipment': self.equipment,
            'rating': self.rating,
            'description': self.description
        }
    
    def get_rating(self):
        return floor(self.rating)