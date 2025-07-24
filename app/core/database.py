from pymongo import MongoClient
from app.core.config import settings

# Simple global database connection
client: MongoClient = None
database = None


def get_database():
    """Get the database instance"""
    if database is None:
        raise RuntimeError("Database not connected")
    return database


def connect_to_mongo():
    """Connect to MongoDB"""
    global client, database
    client = MongoClient(settings.MONGODB_URL)
    database = client[settings.DATABASE_NAME]
    
    # Create indexes
    database["users"].create_index("email", unique=True)
    database["expenses"].create_index([("user_id", 1), ("date", -1)])
    database["expenses"].create_index("category")
    
    print(f"Connected to MongoDB: {settings.DATABASE_NAME}")


def close_mongo_connection():
    """Close MongoDB connection"""
    global client
    if client:
        client.close()
        print("Disconnected from MongoDB")