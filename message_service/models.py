from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(100))
    receiver = db.Column(db.String(100))
    message = db.Column(db.Text)
    probability = db.Column(db.Float)
    status = db.Column(db.String(20))  # "sent" / "not sent"
    note = db.Column(db.Text)
