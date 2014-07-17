import pymongo


client = pymongo.MongoClient("192.168.1.109")

db = client["loghub_dev"]
