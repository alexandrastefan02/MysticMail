from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Message

app = Flask(__name__)
CORS(app)

# Conectare la baza de date mistica 🧙‍♀️
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://mystic:magicpass@db:5432/mysticmail"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# Creează tabelele dacă nu există
with app.app_context():
    db.create_all()
    print("✅ Tabelele au fost create sau există deja.")

@app.route("/", methods=["GET"])
def home():
    return "<h2>✨ MysticMail Message Service is running!</h2>"

@app.route("/send_message", methods=["POST"])
def send_message():
    data = request.json
    new_msg = Message(
        sender=data.get("sender"),
        receiver=data.get("receiver"),
        message=data.get("message"),
        probability=data.get("probability"),
        status="sent"  # pentru test, se poate adăuga random mai târziu
    )
    db.session.add(new_msg)
    db.session.commit()
    return jsonify({"status": "sent", "message_id": new_msg.id})

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005)
