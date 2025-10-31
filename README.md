🧠 MindCare Backend

A robust backend system for MindCare, a web-based platform connecting clients and therapists for mental health support.
This API handles user management, session booking, email notifications, and secure data storage.

🚀 Project Description

MindCare simplifies access to mental health and wellness support by connecting clients with verified therapists and therapy centers.
The backend manages all core functionalities including:

👥 Multi-role system: Clients, Therapists, and Admins

🏥 Therapist & Center Profiles: Managed and verified by Admin

📅 Session Booking: Real-time availability tracking and appointment scheduling

✉️ Automated Email Reminders: Clients receive notifications for upcoming sessions

🧾 Session History: Clients can view and track past sessions

🔒 Secure Authentication: Password hashing, validation, and JWT-based access control

🧰 Admin Dashboard API: Manage users, sessions, and wellness centers

🛠️ Technologies Used

Flask – Web framework for Python

Flask SQLAlchemy – ORM for database management

Flask Bcrypt – For password hashing and secure login

Flask JWT Extended – For user authentication and token management

Flask Mail – For sending automated appointment reminders

SQLite / PostgreSQL – Database support

SQLAlchemy Serializer – For JSON serialization

Marshmallow (optional) – For data validation and schema handling