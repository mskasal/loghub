from loghub.storage import db
from bson.objectid import ObjectId


collection_name = "priviliges"
coll = db[collection_name]


def is_admin(app_id,user_id):
    app_privileges = coll.find_one({
                        "app_id":app_id,
                        "uid":user_id
                         })
    if app_privileges["type"] == "admin":
        return True
    else:
        return False

def is_user(app_id,user_id):
    app_privileges = coll.find_one({
                        "app_id":app_id,
                        "uid":user_id
                        })
    if app_privileges["type"] == "consumer":
        return True
    else:
        return False

def check_user(user_id,app_id):
    app_privileges =  list(coll.find({"uid":user_id,
                                    "app_id":app_id
                                    }))
    if any(str(user_id) in str(i["uid"]) for i in app_privileges):
        return True
    
    return False


def add_user_to_app(user_id, app_id, _type):
    return coll.insert({
            "uid":user_id,
            "app_id":app_id,
            "type": _type
            })


def get_user_apps(user_id):
    app_data = coll.find({"uid":user_id})
    app_id_list = []
    for app in app_data:
        app_id_list.append((app["app_id"]))
    
  
    apps = list(db["apps"].find({
        "_id": {"$in": app_id_list }
        }))

    app_tokens = [ app["APP_TOKEN"] for app in apps]
    
    return app_tokens
