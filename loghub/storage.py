import pymongo


client = pymongo.MongoClient("192.168.1.140")

db = client["loghub_dev"]
