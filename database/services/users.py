from database.database import users_collection

class UsersDB:

    @staticmethod
    def add_user(user_id):
        ...

    @staticmethod
    def get_user(user_id):
        return users_collection.find_one({"telegram_id": user_id})

    @staticmethod
    def ban_user(user_id):
        ...

    @staticmethod
    def verify_user(user_id):
        ...