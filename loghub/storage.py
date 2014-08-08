import pymongo


client = pymongo.MongoClient("192.168.1.122")

db = client["loghub_dev"]
