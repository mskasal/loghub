import pymongo


client = pymongo.MongoClient("192.168.1.125")

db = client["loghub_dev"]
