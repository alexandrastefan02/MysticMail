from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from models import db, Message
import os
import json
import random

from auth import register_user, authenticate_user

from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
app = Flask(__name__)
metrics = PrometheusMetrics(app)
CORS(app)

# Conectare la baza de date mistica 🧙‍♀️
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://mystic:magicpass@db:5432/mysticmail"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# Creează tabelele dacă nu există
with app.app_context():
    db.create_all()
    SENT_NOTES = [
    "✨ Message sent by fate!",
    "💫 Carried by cosmic winds.",
    "🪐 Launched through the void.",
    "🌙 Whispered to the stars.",
    "🔮 Channeled through mystic forces.",
    "📡 Beamed to alternate dimensions.",
    "📜 Written in ancient runes.",
    "🐉 Delivered by dragon post.",
    "🧚‍♀️ Sprinkled with stardust.",
    "⚡ Struck by divine lightning.",
    "💌 A love letter from the beyond.",
    "🧙‍♂️ Cast with arcane magic.",
    "🌈 Found at the end of a rainbow.",
    "🍄 Grown from fungal thoughts.",
    "🌪️ Sent via elemental whirlwind.",
    "🕊️ Flown by celestial pigeon.",
    "🎠 Riding the dream carousel.",
    "🚀 Blasted from a glitter rocket."
    ]

    UNSEND_NOTES = [
        "🌫️ Message lost in the mists...",
        "💨 Whisked away by the wind.",
        "👻 Disappeared into thin air.",
        "❌ Canceled by fate.",
        "💥 Exploded into stardust.",
        "🧿 Hexed out of existence.",
        "⏳ Lost in time.",
        "💔 Broken by cosmic forces.",
        "🔒 Sealed away forever.",
        "🚫 Blocked by the universe.",
    ]
    print("✅ Tabelele au fost create sau există deja.")

@app.route("/", methods=["GET"])
def home():
    return "<h2>✨ MysticMail Message Service is running!</h2>"

@app.route("/send_message", methods=["POST"])
def send_message():
    data = request.json

    sender = data.get("sender")
    receiver = data.get("receiver")
    message = data.get("message")
    probability = data.get("probability", 0.5)

    was_sent = random.random() < probability
    status = "sent" if was_sent else "missed"
    note = random.choice(SENT_NOTES if was_sent else UNSEND_NOTES)

    new_msg = Message(
        sender=sender,
        receiver=receiver,
        message=message,
        probability=probability,
        status=status,
        note=note
    )
    db.session.add(new_msg)
    db.session.commit()

    return jsonify({
        "status": new_msg.status,
        "message_id": new_msg.id,
        "note": new_msg.note
    })


@app.route("/get_messages", methods=["GET"])
def get_messages():
    messages = Message.query.all()
    return jsonify([
        {
            "from": msg.sender,
            "to": msg.receiver,
            "message": msg.message,
            "status": msg.status,
            "note": msg.note
        } for msg in messages
    ])

@app.route("/metrics")
def metrics_endpoint():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005)