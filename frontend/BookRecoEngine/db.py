import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")  # from MongoDB Atlas
DB_NAME = os.getenv("DB_NAME", "book_reco_db")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
users_col = db["users"]

def get_user(user_id: str):
    return users_col.find_one({"_id": user_id})

def upsert_user(user_id: str, data: dict):
    data["_id"] = user_id
    users_col.update_one(
        {"_id": user_id},
        {"$set": data},
        upsert=True
    )

def add_rating(user_id: str, rating_obj: dict):
    users_col.update_one(
        {"_id": user_id},
        {"$push": {"ratings": rating_obj}},
        upsert=True
    )
