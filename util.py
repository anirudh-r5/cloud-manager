import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from os import getenv
from dotenv import load_dotenv
load_dotenv()

MONGO_URI = getenv("DATABASE_URL")

client = AsyncIOMotorClient(MONGO_URI)
db = client.get_default_database()

async def seed():
    # Clear existing data (optional)
    await db.users.delete_many({})
    await db.permissions.delete_many({})
    await db.plans.delete_many({})
    await db.subscriptions.delete_many({})
    await db.usages.delete_many({})

    # Users
    await db.users.insert_many([
        {"username": "admin1", "role": "admin"},
        {"username": "alice", "role": "customer"},
        {"username": "bob", "role": "customer"}
    ])

    # Permissions
    permissions = [
        {"name": "Compute", "endpoint": "/compute", "description": "Virtual CPU service"},
        {"name": "Storage", "endpoint": "/storage", "description": "File storage"},
        {"name": "AI", "endpoint": "/ai", "description": "AI model access"},
        {"name": "App", "endpoint": "/app", "description": "App deployment"},
        {"name": "DB", "endpoint": "/db", "description": "Database service"},
        {"name": "Container", "endpoint": "/container", "description": "Docker container hosting"}
    ]
    await db.permissions.insert_many(permissions)

    # Plans
    pro_plan = {
        "name": "Pro Plan",
        "description": "Access to all services with generous limits",
        "permissions": ["compute", "storage", "container", "db", "app", "ai"],
        "limits": {
            "compute": 100,
            "storage": 200,
            "container": 100,
            "db": 150,
            "app": 75,
            "ai": 50
        }
    }

    basic_plan = {
        "name": "Basic Plan",
        "description": "Limited access to core services",
        "permissions": ["compute", "storage"],
        "limits": {
            "compute": 30,
            "storage": 50
        }
    }

    pro_id = await db.plans.insert_one(pro_plan)
    basic_id = await db.plans.insert_one(basic_plan)

    # Subscriptions
    await db.subscriptions.insert_many([
        {"user_id": "alice", "plan_id": pro_id.inserted_id},
        {"user_id": "bob", "plan_id": basic_id.inserted_id}
    ])

    print("✅ Sample data inserted successfully.")

asyncio.run(seed())

# async def clear_all_data():
#     await db.users.delete_many({})
#     await db.plans.delete_many({})
#     await db.permissions.delete_many({})
#     await db.subscriptions.delete_many({})
#     await db.usages.delete_many({})

#     print("🧹 All sample data cleared.")
# asyncio.run(clear_all_data())