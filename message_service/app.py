from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from auth import register_user, authenticate_user
import random

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
CORS(app)  # 🧙‍♀️ linia magică!

DATA_FILE = "messages.json"
@app.route("/", methods=["GET"])
def home():
    return "<h2>Welcome to MysticMail User Service 🧙‍♀️</h2>"

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "Username and password required"}), 400
    username = data["username"]
    password = data["password"]
    return register_user(username, password)

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "Username and password required"}), 400
    username = data["username"]
    password = data["password"]
    return authenticate_user(username, password)

@app.route("/send_message", methods=["POST"])
def send_message():
    data = request.json

    # Get data from request, set defaults
    probability = data.get("probability", 1)
    send_status = "sent" if random.random() < probability else "not sent"

    # Select note based on whether the message is sent or not
    if send_status == "sent":
        note = random.choice(SENT_NOTES)
    else:
        note = random.choice(UNSEND_NOTES)

    new_message = {
        "from": data.get("from", "mystic"),
        "to": data.get("to", ""),
        "message": data.get("message", ""),
        "probability": probability,
        "note": note,
        "status": send_status
    }

    # Read messages.json or create a new list
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            try:
                messages = json.load(f)
            except json.JSONDecodeError:
                messages = []
    else:
        messages = []

    # Append new message and save
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
