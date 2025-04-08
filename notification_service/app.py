from flask import Flask, request, jsonify
from send_email import send_real_email

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "<h2>📡 MysticMail Notification Service is online</h2>"

@app.route("/notify", methods=["POST"])
def notify():
    data = request.get_json()
    receiver = data.get("receiver")
    message = data.get("message")

    result = send_real_email(receiver, message)
    print("receiver")
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
