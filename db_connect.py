import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
MONGO_CONNECT = os.getenv('MONGODB_CONNECTION')


def connect_db():
    client = MongoClient(MONGO_CONNECT)
    db = client['camarilla']
    return db