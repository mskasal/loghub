import pymongo


#client = pymongo.MongoClient("192.168.1.125")
client = pymongo.MongoClient("localhost")

db = client["loghub_dev"]
