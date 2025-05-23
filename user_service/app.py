from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from models import db, User
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
import hashlib

app = Flask(__name__)
metrics = PrometheusMetrics(app)
CORS(app)  # 🧙‍♀️ linia magică!

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://mystic:magicpass@db:5432/mysticmail"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

created_tables = False

@app.route("/", methods=["GET"])
def home():
    global created_tables
    if not created_tables:
        try:
            with app.app_context():
                db.create_all()
                print("✅ Tables created (or already exist).")
                created_tables = True
        except Exception as e:
            print("❌ Failed to create tables:", e)
    return "<h2>Welcome to MysticMail User Service 🧙‍♀️</h2>"

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "User already exists"}), 400
    user = User(username=data['username'], password_hash=hash_password(data['password']))
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully!"}), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    if user.password_hash != hash_password(data['password']):
        return jsonify({"error": "Incorrect password"}), 401
    return jsonify({"message": "Login successful!"}), 200

@app.route("/metrics")
def metrics_endpoint():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
