from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

# MongoDB Connection
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'spreadsheet_manager')

client = MongoClient(MONGODB_URI)
db = client[DATABASE_NAME]

# Collections
users_collection = db['users']
sessions_collection = db['sessions']

# Create indexes
users_collection.create_index('email', unique=True)
users_collection.create_index('google_id', unique=True, sparse=True)

def get_db():
    return db

def get_users_collection():
    return users_collection

def get_sessions_collection():
    return sessions_collection
