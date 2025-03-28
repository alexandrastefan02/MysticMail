from flask import Flask, request, jsonify
from flask_cors import CORS
from auth import register_user, authenticate_user

app = Flask(__name__)
CORS(app)  # 🧙‍♀️ linia magică!


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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
