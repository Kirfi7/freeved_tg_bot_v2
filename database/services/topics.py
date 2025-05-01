from database.database import topics_collection

class TopicsDB:

    @staticmethod
    def init_topic(topic_id: int, user_id: int):
        return topics_collection.insert_one({
            "topic_id": topic_id, "user_id": user_id
        })

    @staticmethod
    def get_topic_by_user(user_id: int):
        if topic := topics_collection.find_one({"user_id": user_id}):
            return topic.get("topic_id")

    @staticmethod
    def get_user_by_topic(topic_id: int):
        if topic := topics_collection.find_one({"topic_id": topic_id}):
            return topic.get("user_id")