from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
import redis
import json
from prometheus_client import generate_latest, Counter

app = Flask(__name__)

# MongoDB connection setup
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://kathankathrotiya:Kathan@cluster0.kg7k2cr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DATABASE_NAME = "user_service_db"

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
user_collection = db["users"]

# Redis connection setup
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

# Redis Pub/Sub channel
CHANNEL_NAME = "crud_notifications"

# Define a counter metric to track requests
REQUEST_COUNT = Counter('request_count', 'Total number of requests')

# Metrics endpoint
@app.route('/metrics')
def metrics():
    return generate_latest(), 200

# Helper function to serialize MongoDB documents
def user_serializer(user) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "address": user.get("address"),
    }

# Publish a CRUD event to Redis
def publish_crud_event(action, data):
    event = {
        "action": action,
        "service": "user_service",
        "data": data
    }
    redis_client.publish(CHANNEL_NAME, json.dumps(event))

# Create a new user
@app.route("/user", methods=["POST"])
def create_user():
    data = request.get_json()
    new_user = {
        "name": data["name"],
        "email": data["email"],
        "address": data.get("address")
    }
    result = user_collection.insert_one(new_user)
    created_user = user_collection.find_one({"_id": result.inserted_id})
    # Publish the create event
    publish_crud_event("create", user_serializer(created_user))
    return jsonify(user_serializer(created_user)), 201

# Retrieve a user by ID
@app.route("/user/<user_id>", methods=["GET"])
def get_user(user_id):
    user = user_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        return jsonify(user_serializer(user))
    else:
        return jsonify({"error": "User not found"}), 404

# Update an existing user by ID
@app.route("/user/<user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()
    updated_data = {
        "name": data["name"],
        "email": data["email"],
        "address": data.get("address")
    }
    result = user_collection.update_one(
        {"_id": ObjectId(user_id)}, {"$set": updated_data}
    )
    if result.modified_count > 0:
        updated_user = user_collection.find_one({"_id": ObjectId(user_id)})
        # Publish the update event
        publish_crud_event("update", user_serializer(updated_user))
        return jsonify(user_serializer(updated_user))
    else:
        return jsonify({"error": "User not found or not modified"}), 404

# Delete a user by ID
@app.route("/user/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    result = user_collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count > 0:
        # Publish the delete event
        publish_crud_event("delete", {"id": user_id})
        return jsonify({"message": "User deleted successfully"})
    else:
        return jsonify({"error": "User not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=50053, debug=True)
