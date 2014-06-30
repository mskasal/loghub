import pymongo

client = pymongo.MongoClient("192.168.1.131")

db = client["loghub_dev"]
