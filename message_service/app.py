from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import os
import json
import random

from auth import register_user, authenticate_user

from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

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
    "🚫 Blocked by the universe."
]

app = Flask(__name__)
metrics = PrometheusMetrics(app)
CORS(app)


DATA_FILE = "messages.json"

@app.route("/", methods=["GET"])
def home():
    return "<h2>Welcome to MysticMail Message Service 🚀</h2>"

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "Username and password required"}), 400
    return register_user(data["username"], data["password"])

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "Username and password required"}), 400
    return authenticate_user(data["username"], data["password"])

@app.route("/send_message", methods=["POST"])
def send_message():
    data = request.json
    probability = data.get("probability", 1)
    send_status = "sent" if random.random() < probability else "not sent"
    note = random.choice(SENT_NOTES if send_status == "sent" else UNSEND_NOTES)

    new_message = {
        "from": data.get("from", "mystic"),
        "to": data.get("to", ""),
        "message": data.get("message", ""),
        "probability": probability,
        "note": note,
        "status": send_status
    }

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            try:
                messages = json.load(f)
            except json.JSONDecodeError:
                messages = []
    else:
        messages = []

    messages.append(new_message)
    with open(DATA_FILE, 'w') as f:
        json.dump(messages, f)

    return jsonify(new_message)

@app.route("/get_messages", methods=["GET"])
def get_messages():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            try:
                messages = json.load(f)
            except json.JSONDecodeError:
                messages = []
    else:
        messages = []
    return jsonify(messages)

@app.route("/metrics")
def metrics_endpoint():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)



