import pymongo
from datetime import datetime
from config import MONGODB_URI

# Initialize MongoDB connection
client = pymongo.MongoClient(MONGODB_URI)
db = client['terabox_aditya_singh']

# Collections
users_collection = db['users']
channels_collection = db['channels']

def store_user_info(user_id, username, first_name):
    """Store user information in the database"""
    if not users_collection.find_one({"user_id": user_id}):
        user_data = {
            "user_id": user_id,
            "username": username,
            "first_name": first_name
        }
        users_collection.insert_one(user_data)

async def fetch_all_users():
    """Fetch all user IDs from the database"""
    users = users_collection.find()
    return [user['user_id'] for user in users]

def update_force_sub_channel(channel_id, channel_title, channel_username=None, invite_link=None):
    """Update force subscription channel in database"""
    channels_collection.update_one(
        {"type": "force_sub"},
        {
            "$set": {
                "channel_id": channel_id,
                "is_default": False,
                "last_updated": datetime.now(),
                "channel_title": channel_title,
                "channel_username": channel_username,
                "is_private": not bool(channel_username),
                "invite_link": invite_link
            }
        },
        upsert=True
    )

def get_force_sub_channel():
    """Get current force subscription channel"""
    return channels_collection.find_one({"type": "force_sub"}) 