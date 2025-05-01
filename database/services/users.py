from database.database import users_collection
from database.models import User

class UsersDB:

    @staticmethod
    def add_user(account_data: User):
        return users_collection.insert_one(account_data.model_dump())

    @staticmethod
    def get_user(user_id):
        return users_collection.find_one({"telegram_id": user_id})

    @staticmethod
    def ban_user(user_id):
        return users_collection.update_one(
            {"telegram_id": user_id},
            {"$set": {"is_banned": True}}
        )

    @staticmethod
    def verify_user(user_id):
        return users_collection.update_one(
            {"telegram_id": user_id},
            {"$set": {"is_verified": True}}
        )