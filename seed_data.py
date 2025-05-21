############################
# !NOT REQUIRED IN PRODUCTION (OPTIONAL)
############################


from models import db, User, UserProfile, MentalHealthAssessment, HabitTracker, Appointment, Psychologist, JournalEntry
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import random

def create_seed_data(app):
    with app.app_context():
        # Check if data already exists
        if User.query.count() > 0:
            print("Seed data already exists")
            return
        
        print("Creating seed data...")
        
        # Create users
        users = [
            User(
                usn="admin",
                pas=generate_password_hash("admin123"),
                email="admin@mindcare.com",
                date_registered=datetime.utcnow(),
                last_login=datetime.utcnow()
            ),
            User(
                usn="john",
                pas=generate_password_hash("john123"),
                email="john@mindcare.com",
                date_registered=datetime.utcnow() - timedelta(days=10),
                last_login=datetime.utcnow() - timedelta(days=2)
            ),
            User(
                usn="sarah",
                pas=generate_password_hash("sarah123"),
                email="sarah@mindcare.com",
                date_registered=datetime.utcnow() - timedelta(days=15),
                last_login=datetime.utcnow() - timedelta(days=1)
            ),
            User(
                usn="mike",
                pas=generate_password_hash("mike123"),
                email="mike@mindcare.com",
                date_registered=datetime.utcnow() - timedelta(days=5),
                last_login=datetime.utcnow() - timedelta(hours=12)
            ),
            User(
                usn="emma",
                pas=generate_password_hash("emma123"),
                email="emma@mindcare.com",
                date_registered=datetime.utcnow() - timedelta(days=20),
                last_login=datetime.utcnow() - timedelta(days=3)
            )
        ]
        
        db.session.add_all(users)
        db.session.commit()
        
        # Create user profiles
        profiles = [
            UserProfile(
                user_id=1,
                full_name="Admin User",
                age=30,
                gender="Other",
                phone="555-1234",
                address="123 Admin St, Tech City",
                bio="System administrator for MindCare platform",
                profile_picture="profile1.jpg"
            ),
            UserProfile(
                user_id=2,
                full_name="John Smith",
                age=25,
                gender="Male",
                phone="555-5678",
                address="456 Oak Ave, Woodland",
                bio="Software developer dealing with work stress and anxiety",
                profile_picture="profile2.jpg"
            ),
            UserProfile(
                user_id=3,
                full_name="Sarah Johnson",
                age=28,
                gender="Female",
                phone="555-9012",
                address="789 Pine St, Lakeside",
                bio="Teacher experiencing burnout and seeking better work-life balance",
                profile_picture="profile3.jpg"
            ),
            UserProfile(
                user_id=4,
                full_name="Mike Wilson",
                age=32,
                gender="Male",
                phone="555-3456",
                address="101 Maple Dr, Riverside",
                bio="Marketing executive with insomnia and stress management issues",
                profile_picture="profile4.jpg"
            ),
            UserProfile(
                user_id=5,
                full_name="Emma Davis",
                age=24,
                gender="Female",
                phone="555-7890",
                address="202 Elm St, Hillside",
                bio="Graduate student dealing with academic pressure and anxiety",
                profile_picture="profile5.jpg"
            )
        ]
        
        db.session.add_all(profiles)
        db.session.commit()
        
        # Create psychologists
        psychologists = [
            Psychologist(
                name="Dr. Emily Chen",
                specialization="Anxiety Disorders",
                email="dr.chen@mindcare.com",
                phone="555-2468",
                bio="Specializes in treating anxiety and panic disorders with 10+ years of experience",
                availability="Monday, Wednesday, Friday: 9AM-5PM"
            ),
            Psychologist(
                name="Dr. Michael Brown",
                specialization="Depression",
                email="dr.brown@mindcare.com",
                phone="555-1357",
                bio="Expert in treating depression and mood disorders using cognitive behavioral therapy",
                availability="Tuesday, Thursday: 10AM-6PM"
            ),
            Psychologist(
                name="Dr. Lisa Rodriguez",
                specialization="Stress Management",
                email="dr.rodriguez@mindcare.com",
                phone="555-8642",
                bio="Focuses on stress management techniques and mindfulness-based therapies",
                availability="Monday, Tuesday, Thursday: 8AM-4PM"
            )
        ]
        
        db.session.add_all(psychologists)
        db.session.commit()
        
        # Create mental health assessments
        stress_levels = ["Low", "Moderate", "High", "Severe"]
        
        assessments = []
        for user_id in range(2, 6):
            # Create 2 assessments per user
            for i in range(2):
                days_ago = random.randint(1, 30)
                assessments.append(
                    MentalHealthAssessment(
                        user_id=user_id,
                        assessment_date=datetime.utcnow() - timedelta(days=days_ago),
                        stress_level=random.choice(stress_levels),
                        anxiety_level=random.randint(1, 10),
                        depression_level=random.randint(1, 10),
                        notes=f"Assessment #{i+1} - Patient shows signs of {random.choice(['work-related stress', 'anxiety', 'mild depression', 'sleep disturbance'])}"
                    )
                )
        
        db.session.add_all(assessments)
        db.session.commit()
        
        # Create habit tracking entries
        habit_names = ["Meditation", "Exercise", "Journaling", "Deep Breathing", "Reading", "Yoga"]
        
        habits = []
        for user_id in range(2, 6):
            # Create 3-5 habits per user
            for i in range(random.randint(3, 5)):
                days_ago = random.randint(0, 14)
                habits.append(
                    HabitTracker(
                        user_id=user_id,
                        habit_name=random.choice(habit_names),
                        date_performed=datetime.utcnow() - timedelta(days=days_ago),
                        duration_minutes=random.randint(10, 60),
                        notes=f"Session {i+1} - {random.choice(['Morning', 'Afternoon', 'Evening'])} routine"
                    )
                )
        
        db.session.add_all(habits)
        db.session.commit()
        
        # Create appointments
        appointment_statuses = ["scheduled", "completed", "cancelled"]
        
        appointments = []
        for user_id in range(2, 6):
            # Create 1-2 appointments per user
            for i in range(random.randint(1, 2)):
                days_offset = random.randint(-10, 10)  # Past or future appointments
                psychologist_id = random.randint(1, 3)
                
                # Set status based on date
                if days_offset < 0:
                    status = random.choice(["completed", "cancelled"])
                else:
                    status = "scheduled"
                
                appointments.append(
                    Appointment(
                        user_id=user_id,
                        psychologist_id=psychologist_id,
                        appointment_date=datetime.utcnow() + timedelta(days=days_offset),
                        status=status,
                        notes=f"{random.choice(['Initial consultation', 'Follow-up session', 'Therapy session', 'Check-in meeting'])}"
                    )
                )
        
        db.session.add_all(appointments)
        db.session.commit()
        
        # Create journal entries
        moods = ["Happy", "Sad", "Anxious", "Calm", "Stressed", "Hopeful", "Frustrated", "Motivated"]
        feeling_texts = [
            "I practiced some breathing exercises.",
            "I went for a walk to clear my head.",
            "I talked with a friend about my feelings.",
            "I tried to focus on positive thoughts."
        ]
        conclusion_texts = [
            "Tomorrow will be better.",
            "I need to keep working on my mental health.",
            "I feel like I am making progress.",
            "I am grateful for the support I have."
        ]

        journals = []
        for user_id in range(2, 6):
            # Create 2-4 journal entries per user
            for i in range(random.randint(2, 4)):
                days_ago = random.randint(0, 30)
                mood = random.choice(moods)
                feeling = random.choice(feeling_texts)
                conclusion = random.choice(conclusion_texts)
                
                content = f"Today I felt {mood.lower()}. {feeling} {conclusion}"
                
                journals.append(
                    JournalEntry(
                        user_id=user_id,
                        entry_date=datetime.utcnow() - timedelta(days=days_ago),
                        title=f"Day {i+1}: Feeling {mood}",
                        content=content,
                        mood=mood
                    )
                )
        
        db.session.add_all(journals)
        db.session.commit()
        
        print("Seed data created successfully!")
