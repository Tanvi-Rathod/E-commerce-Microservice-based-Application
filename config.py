from pymongo import MongoClient
from os import getenv

MONGO_URI = getenv("MONGO_URI", "mongodb://localhost:27017/")
DATABASE_NAME = "user_service_db"

client = MongoClient(MONGO_URI)
database = client[DATABASE_NAME]
user_collection = database["users"]
