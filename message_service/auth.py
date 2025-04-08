import hashlib
from flask import jsonify

# Simulăm o bază de date simplă (temporar, in-memory)
users = {}

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    if username in users:
        return jsonify({"error": "User already exists"}), 400
    users[username] = hash_password(password)
    return jsonify({"message": "User registered successfully!"}), 201

def authenticate_user(username, password):
    if username not in users:
        return jsonify({"error": "User not found"}), 404
    if users[username] != hash_password(password):
        return jsonify({"error": "Incorrect password"}), 401
    return jsonify({"message": "Login successful!"}), 200
