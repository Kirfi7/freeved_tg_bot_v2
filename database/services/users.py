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
    def unban_user(user_id: int):
        return users_collection.update_one(
            {"telegram_id": user_id},
            {"$set": {"is_banned": False}}
        )

    @staticmethod
    def is_banned(user_id):
        if user := users_collection.find_one({"telegram_id": user_id}):
            return user.get("is_banned") or False
        return False

    @staticmethod
    def get_autopublish_count(user_id: int) -> int:
        user = users_collection.find_one({"telegram_id": user_id})
        if not user:
            return 0
        return int(user.get("autopublish_count") or 0)

    @staticmethod
    def inc_autopublish_count(user_id: int, delta: int = 1):
        return users_collection.update_one(
            {"telegram_id": user_id},
            {"$inc": {"autopublish_count": delta}},
            upsert=True,
        )

    @staticmethod
    def reset_autopublish_count(user_id: int):
        return users_collection.update_one(
            {"telegram_id": user_id},
            {"$set": {"autopublish_count": 0}},
            upsert=True,
        )
