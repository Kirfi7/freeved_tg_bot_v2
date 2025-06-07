from database.database import users_collection, posts_collection
from database.models import User

class UsersDB:

    @staticmethod
    def add_user(account_data: User):
        return users_collection.insert_one(account_data.model_dump())

    @staticmethod
    def get_user(user_id):
        return users_collection.find_one({"telegram_id": user_id})

    @staticmethod
    def get_messages_count(user_id):
        return posts_collection.count_documents({"author_id": user_id, "is_published": True})

    @staticmethod
    def ban_user(user_id):
        return users_collection.update_one(
            {"telegram_id": user_id},
            {"$set": {"is_banned": True}}
        )

    @staticmethod
    def is_banned(user_id):
        if user := users_collection.find_one({"telegram_id": user_id}):
            return user.get("is_banned") or False
        return False

    @staticmethod
    def verify_user(user_id):
        return users_collection.update_one(
            {"telegram_id": user_id},
            {"$set": {"is_verified": True}}
        )