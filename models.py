from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

# User Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    usn = db.Column(db.String(20), unique=True)
    pas = db.Column(db.String(1000))
    email = db.Column(db.String(100), unique=True, nullable=True)
    date_registered = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

# UserProfile model
class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    full_name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    bio = db.Column(db.Text)
    profile_picture = db.Column(db.String(200))  # Path to profile picture
    
    user = db.relationship('User', backref=db.backref('profile', uselist=False))

# Mental health assessment model
class MentalHealthAssessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    assessment_date = db.Column(db.DateTime, default=datetime.utcnow)
    stress_level = db.Column(db.String(20))
    anxiety_level = db.Column(db.Integer)
    depression_level = db.Column(db.Integer)
    notes = db.Column(db.Text)
    
    user = db.relationship('User', backref=db.backref('assessments', lazy=True))

# Habit tracking model
class HabitTracker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    habit_name = db.Column(db.String(100), nullable=False)
    date_performed = db.Column(db.DateTime, default=datetime.utcnow)
    duration_minutes = db.Column(db.Integer)
    notes = db.Column(db.Text)
    
    user = db.relationship('User', backref=db.backref('habits', lazy=True))

# Appointment booking model
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    psychologist_id = db.Column(db.Integer, db.ForeignKey('psychologist.id'), nullable=False)
    appointment_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='scheduled')  # scheduled, completed, cancelled
    notes = db.Column(db.Text)
    
    user = db.relationship('User', backref=db.backref('appointments', lazy=True))
    psychologist = db.relationship('Psychologist', backref=db.backref('appointments', lazy=True))

# Psychologist model for appointment bookings
class Psychologist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(20))
    bio = db.Column(db.Text)
    availability = db.Column(db.Text)  # JSON string with availability schedule
    
# Journal entries for users to record thoughts and feelings
class JournalEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    entry_date = db.Column(db.DateTime, default=datetime.utcnow)
    title = db.Column(db.String(200))
    content = db.Column(db.Text, nullable=False)
    mood = db.Column(db.String(50))
    
    user = db.relationship('User', backref=db.backref('journal_entries', lazy=True))
