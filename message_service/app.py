from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from models import db, Message
import os
import json
import random
import time
import psycopg2
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from mailgun_client import send_simple_message
app = Flask(__name__)
metrics = PrometheusMetrics(app)
CORS(app)

# Conectare la baza de date mistica 🧙‍♀️
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://mystic:magicpass@db:5432/mysticmail"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# Asigură-te că baza de date e disponibilă și creează tabelele
with app.app_context():
    def wait_for_db():
        while True:
            try:
                conn = psycopg2.connect("dbname='mysticmail' user='mystic' host='db' password='magicpass'")
                conn.close()
                print("✅ Baza de date e gata!")
                break
            except psycopg2.OperationalError:
                print("⏳ Aștept baza de date...")
                time.sleep(2)
    wait_for_db()
    db.create_all()
    print("✅ Tabelele au fost create sau există deja.")

SENT_NOTES = [
    "✨ Message sent by fate!",
    "💫 Carried by cosmic winds.",
    # ... (restul listelor)
]

UNSEND_NOTES = [
    "🌫️ Message lost in the mists...",
    # ... (restul listelor)
]

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
    if was_sent:
        resp = send_simple_message(receiver, message)
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
