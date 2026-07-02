from pymongo import MongoClient

from config import get_env


client = MongoClient(get_env("MONGO_URI", "mongodb://localhost:27017/"))

db = client[get_env("MONGO_DB_NAME", "user_database")]
collection = db[get_env("MONGO_COLLECTION_NAME", "users")]
