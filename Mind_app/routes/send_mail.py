from flask import Blueprint
from flask_mail import Mail, Message
import os

send_bp = Blueprint("send_bp", __name__)

mail = Mail()

def init_mail(app):
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'sandbox.smtp.mailtrap.io')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 2525))
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', 'your_mailtrap_username')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', 'your_mailtrap_password')
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    mail.init_app(app)

@send_bp.route('/send')
def send_email():
    message = Message(
        subject="Hello from MindCare App",
        recipients=["test.mailtrap1234@gmail.com"],
        sender=('Paul from MindCare', 'paul@mailtrap.club')
    )
    message.body = "This is a test email sent from the MindCare Flask application using Mailtrap."
    mail.send(message)
    return "✅ Email sent successfully!"
