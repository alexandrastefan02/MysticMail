import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

def _read_secret(path):
    try:
        with open(path, "r") as f:
            return f.read().strip()
    except OSError:
        return None

# First, try ENV; if not set, fall back to Docker Secret file
MAILGUN_API_KEY = (
    os.getenv("MAILGUN_API_KEY")
    or _read_secret(os.getenv("MAILGUN_API_KEY_FILE", "/run/secrets/mailgun_api_key"))
)
MAILGUN_DOMAIN = (
    os.getenv("MAILGUN_DOMAIN")
    or _read_secret(os.getenv("MAILGUN_DOMAIN_FILE", "/run/secrets/mailgun_domain"))
)

def send_simple_message(recv, message):
    print("📤 Sending message to Mailgun...", flush=True)
    print("MAILGUN_API_KEY:", "[redacted]" if MAILGUN_API_KEY else None, flush=True)
    print("MAILGUN_DOMAIN:", MAILGUN_DOMAIN, flush=True)

    return requests.post(
        f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
        auth=("api", MAILGUN_API_KEY),
        data={
            "from": f"MysticMail <postmaster@{MAILGUN_DOMAIN}>",
            "to": recv,
            "subject": "MysticMail Message",
            "text": message
        }
    )

@app.route("/", methods=["GET"])
def home():
    return "<h2>📨 MysticMail Notification Service is running!</h2>"

@app.route("/send_email", methods=["POST"])
def send_email():
    data = request.json
    recv = data.get("to")
    message = data.get("message")

    if not recv or not message:
        return jsonify({
            "status": "error",
            "message": "Missing 'to' or 'message'"
        }), 400

    response = send_simple_message(recv, message)

    if response.status_code == 200:
        return jsonify({"status": "sent"}), 200
    else:
        return jsonify({
            "status": "error",
            "code": response.status_code,
            "text": response.text
        }), 500

if __name__ == "__main__":
    print("⚡ Starting Flask on 0.0.0.0:5010")
    app.run(host="0.0.0.0", port=5010)
