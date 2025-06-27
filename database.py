import pymongo
from datetime import datetime
import bcrypt

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client['AivaDB']
user_collection = db['users']
chat_collection = db['chats']


def savechat(username, message, aiva_response):
    chat_data = {
        "username": username,
        "message": message,
        "aiva_response": aiva_response,
        "time": datetime.now()
    }
    chat_collection.insert_one(chat_data)
    print("Chat saved successfully.")


def getchathistory(username):
    return list(chat_collection.find({"username": username}, {"_id": 0}))


def add_user(username, password):
    existing_user = user_collection.find_one({"username": username})
    if existing_user:
        return "Username already exists."

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user_collection.insert_one({"username": username, "password": hashed_password})
    return "User registered successfully."


def verify_user(username, password):

    user = user_collection.find_one({"username": username})
    if user and bcrypt.checkpw(password.encode('utf-8'), user["password"]):
        return True
    return False
