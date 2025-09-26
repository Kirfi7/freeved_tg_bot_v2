from database.database import posts_collection
from database.models import Post, PostInit

class PostsDB:

    @staticmethod
    def init_post(data: PostInit):
        max_doc = posts_collection.find_one(sort=[("id", -1)])
        post_id = max_doc['id'] + 1 if max_doc else 1
        insert_data = Post(**data.model_dump(), id=post_id)
        posts_collection.insert_one(insert_data.model_dump())
        return post_id

    @staticmethod
    def publish_post(post_id: int, telegram_id: int):
        posts_collection.update_one({"id": post_id}, {"$set": {
            "telegram_id": telegram_id, "is_published": True
        }})

    @staticmethod
    def get_post(post_id: int) -> Post:
        return posts_collection.find_one({"id": post_id})

    @staticmethod
    def get_post_by_tg(tg_post_id: int) -> Post:
        return posts_collection.find_one({"telegram_id": tg_post_id})

    @staticmethod
    def del_post(post_id: int):
        return posts_collection.delete_one({"id": post_id})

    @staticmethod
    def add_post_sub(post_id: int, telegram_id: int):
        posts_collection.update_one(
            {'id': post_id},
            {'$push': {'comment_subscribers': telegram_id}}
        )

    @staticmethod
    def get_post_subs(post_id: int):
        post = posts_collection.find_one({"id": post_id})
        return post.get('comment_subscribers')