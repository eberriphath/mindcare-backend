from faker import Faker
from model import User, Client, Admin, Therapist, Notification, Centre, Session, Progress, db
from app import app
from flask_bcrypt import Bcrypt
import random
from datetime import datetime, timezone

fake = Faker()
bcrypt = Bcrypt(app)

with app.app_context():
    db.drop_all()
    db.create_all()

    centres = []
    for _ in range(3):
        centre = Centre(
            name=fake.company(),
            address=fake.address(),
            town=fake.city(),
            contact=fake.phone_number(),
            description=fake.sentence(nb_words=10),
            latitude=float(fake.latitude()),
            longitude=float(fake.longitude())
        )
        db.session.add(centre)
        centres.append(centre)
    db.session.commit()

    users = []
    for _ in range(15):
        pwd = "password123"
        user = User(
            full_name=fake.name(),
            email=fake.email(),
            password_hash=bcrypt.generate_password_hash(pwd).decode("utf-8"),
            role=random.choice(["client", "admin", "therapist"]),
            created_at=fake.date_time_this_year()
        )
        db.session.add(user)
        users.append(user)
    db.session.commit()

    clients, therapists, admins = [], [], []

    for u in users:
        if u.role == "client":
            client = Client(
                user_id=u.id,
                date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=60),
                contact=fake.phone_number(),
                gender=random.choice(["Male", "Female"])
            )
            db.session.add(client)
            clients.append(client)

        elif u.role == "therapist":
            therapist = Therapist(
                user_id=u.id,
                specialization=fake.job(),
                experience_years=random.randint(1, 20),
                availability=random.choice([True, False]),
                centre_id=random.choice(centres).id
            )
            db.session.add(therapist)
            therapists.append(therapist)

        elif u.role == "admin":
            admin = Admin(
                user_id=u.id,
                permissions="Manage users and oversee sessions"
            )
            db.session.add(admin)
            admins.append(admin)

    db.session.commit()

    sessions = []
    for _ in range(15):
        if not clients or not therapists:
            continue
        session = Session(
            time=fake.date_time_this_month(),
            date=fake.date_this_month(),
            status=random.choice(["scheduled", "completed", "canceled"]),
            client_id=random.choice(clients).id,
            therapist_id=random.choice(therapists).id,
            centre_id=random.choice(centres).id,
            created_at=datetime.now(timezone.utc)
        )
        db.session.add(session)
        sessions.append(session)
    db.session.commit()

    progress = []
    for _ in range(10):
        if not sessions:
            continue
        progress = Progress(
            mood=random.choice(["Happy", "Neutral", "Sad", "Anxious", "Motivated"]),
            reflections=fake.text(200),
            client_id=random.choice(clients).id,
            session_id=session.id,
            created_at=datetime.now(timezone.utc)
        )
        db.session.add(progress)
    db.session.commit()

    notifications = []
    notification_types = ["Session Reminder", "New Message", "Progress Update", "Admin Alert"]
    for _ in range(20):
        notification = Notification(
            user_id=user.id,
                message=fake.sentence(nb_words=10),
                type=random.choice(notification_types),
                status=random.choice(["read", "unread"]),
                created_at=datetime.now(timezone.utc)
            )
        db.session.add(notification)
        notifications.append(notification)
    db.session.commit()

    print("Database seeded successfully.")
