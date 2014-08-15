import pymongo


client = pymongo.MongoClient("localhost")


db = client["loghub_dev"]
