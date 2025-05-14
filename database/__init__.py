from motor.motor_asyncio import AsyncIOMotorClient
from os import getenv
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = getenv("DATABASE_URL")
client = None

async def connect_to_mongo():
    global client
    client = AsyncIOMotorClient(MONGO_URL)
    try:
    	# Perform a ping to verify connection
        await client.admin.command("ping")
        print("✅ Successfully connected to MongoDB.")
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        raise RuntimeError("Could not connect to MongoDB")

def get_db():
    if client is None:
        raise RuntimeError("MongoDB client not initialized. Did you forget to call connect_to_mongo?")
    return client.get_default_database()