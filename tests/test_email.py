from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'gitongawachira76@gmail.com'
app.config['MAIL_PASSWORD'] = 'hezimcjxeextvzms'
app.config['MAIL_DEFAULT_SENDER'] = 'your-email@gmail.com'

mail = Mail(app)

with app.app_context():
    msg = Message('Test Email', recipients=['your-email@gmail.com'])
    msg.body = 'This is a test email from Flask!'
    mail.send(msg)

print("✅ Email sent successfully!")
