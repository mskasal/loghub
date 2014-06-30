import time
from datetime import datetime
import hashlib
import math

from loghub.storage import db
from previleges import*


collection_name = "apps"
coll = db[collection_name]



def register_app(name,credential_id):    
    APP_TOKEN = hashlib.md5((name + credential_id).encode('utf8')).hexdigest()
    coll.insert({
        "name":name,
        "APP_TOKEN": APP_TOKEN,
        "createdAt": datetime.utcnow()
        }
        )

def get_apps(credential_id):
    print db["users"].count()
    user = db["users"].find_one({
                "credential_id":credential_id
                })
    print user
    user_id = user["_id"]
    app_ids = get_user_apps(user_id)
    app_list = []
    for app_id in app_ids:
        application = col.find_one({
            "id":app_id
            })
        app_list.append(application)
        
    return app_list


def delete_apps(APP_TOKEN,credential_id):
    user = db["users"].find_one({
                "credential_id":credential_id
                })
    user_id = user["id"]
    app = coll.find_one({
           "APP_TOKEN":APP_TOKEN,
            })
    app_id = app["id"]
    try:
        if is_admin(app_id, user_id):
            coll.remove(app)
            return True
    except:
        return False
    return False

    
def reset_app_token(old_app_token,credential_id):    
    record = coll.find_one({"APP_TOKEN":old_app_token})    
    variable = str(math.floor(time.time())    )
    NEW_APP_TOKEN = hashlib.md5((record["name"] + credential_id + variable).encode('utf8')).hexdigest()
    record["APP_TOKEN"] = NEW_APP_TOKEN
    return coll.save(record)


#register_app("selam","4")
#print len(get_apps("1"))
#delete_apps("ea28414aff1cf6ad599ad74dc7c14599","1")
#get_apps("2")
#reset_app_token("a577b6ed4a40af193dca7376c6081957","2")
#get_apps("2")