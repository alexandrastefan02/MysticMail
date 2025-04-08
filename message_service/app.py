from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from models import db, Message
import random

# ✨ Note magice pentru livrare
SENT_NOTES = [
    "✨ Message sent by fate!",
    "💫 Carried by cosmic winds.",
    "🪐 Launched through the void.",
    "🌙 Whispered to the stars.",
]

UNSEND_NOTES = [
    "🌫️ Message lost in the mists...",
    "💨 Whisked away by the wind.",
    "❌ Canceled by fate.",
    "👻 Disappeared into thin air.",
]

app = Flask(__name__)
CORS(app)

# Configurare PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://mystic:magicpass@db:5432/mysticmail'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Creăm tabelele dacă nu există
with app.app_context():
    db.create_all()

@app.route("/", methods=["GET"])
def home():
    return "<h2>Welcome to MysticMail Message Service 🌌</h2>"

@app.route("/send_message", methods=["POST"])
def send_message():
    data = request.get_json()
    probability = float(data.get("probability", 1.0))

    sent = random.random() < probability
    status = "sent" if sent else "not sent"
    note = random.choice(SENT_NOTES if sent else UNSEND_NOTES)

    msg = Message(
        sender=data.get("sender"),
        receiver=data.get("receiver"),
        message=data.get("message"),
        probability=probability,
        status=status,
        note=note
    )

    db.session.add(msg)
    db.session.commit()

    return jsonify({
        "message": msg.message,
        "from": msg.sender,
        "to": msg.receiver,
        "probability": msg.probability,
        "status": msg.status,
        "note": msg.note
    })

@app.route("/get_messages", methods=["GET"])
def get_messages():
    messages = Message.query.all()
    return jsonify([
        {
            "from": m.sender,
            "to": m.receiver,
            "message": m.message,
            "probability": m.probability,
            "status": m.status,
            "note": m.note
        }
        for m in messages
    ])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
