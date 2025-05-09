from database.database import posts_collection
from database.models import Post, PostInit

class PostsDB:

    @staticmethod
    def init_post(data: PostInit):
        post_id: int = (posts_collection.find_one({}, {"sort": {"id": -1}})).get("id")
        insert_data = Post(**data.model_dump(), id=post_id)
        posts_collection.insert_one(insert_data.model_dump())

    @staticmethod
    def publish_post(post_id: int, telegram_id: int):
        posts_collection.update_one({"id": post_id}, {"$set": {
            "telegram_id": telegram_id, "is_published": True
        }})

    @staticmethod
    def get_post(post_id: int):
        return posts_collection.find_one({"id": post_id})

    @staticmethod
    def del_post(post_id: int):
        return posts_collection.delete_one({"id": post_id})