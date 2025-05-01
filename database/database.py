import sys
import pymongo

# Подключение к MongoDB
uri = f"mongodb://127.0.0.1:12341/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.1.5"
try:
    client = pymongo.MongoClient(uri)
    print("Соединение с БД установлено успешно!")
except pymongo.errors.ConfigurationError:
    print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
    sys.exit(1)

db = client.myDatabase

users_collection_name = "users"
if users_collection_name not in db.list_collection_names():
    db.create_collection(users_collection_name)
users_collection = db[users_collection_name]

topics_collection_name = "topics"
if topics_collection_name not in db.list_collection_names():
    db.create_collection(topics_collection_name)
topics_collection = db[topics_collection_name]


# collection_messages = "messages"
# if collection_messages not in db.list_collection_names():
#     db.create_collection(collection_messages)
# messages_collection = db[collection_messages]
#
# collection_admins = "admins"
# if collection_admins not in db.list_collection_names():
#     db.create_collection(collection_admins)
# admins_collection = db[collection_admins]
#
# collection_blacklist = "blacklist"
# if collection_blacklist not in db.list_collection_names():
#     db.create_collection(collection_blacklist)
# blacklist_collection = db[collection_blacklist]
#
# collection_waiting = "waiting"
# if collection_waiting not in db.list_collection_names():
#     db.create_collection(collection_waiting)
# waiting_collection = db[collection_waiting]
