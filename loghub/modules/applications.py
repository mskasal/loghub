import time
from datetime import datetime
import hashlib
import math

from loghub.storage import db
from privileges import*
from loghub.workers.applications import applications as c 

collection_name = "apps"
coll = db[collection_name]

@c.task(name="loghub.modules.applications.register_app")
def register_app(name,credential_id):
    if not name and not credential_id:
        return 41
    if not name:
        return 42
    if not credential_id:
        return 43

    APP_TOKEN = hashlib.md5((name + credential_id).encode('utf8')).hexdigest()
    app_id = coll.insert({
            "name":name,
            "APP_TOKEN": APP_TOKEN,
            "createdAt": datetime.utcnow()
            }
            )
    user_id = db["users"].find_one({"credential_id":credential_id })["_id"]
    if not user_id:
        return 44
    
    add_user_to_app(user_id,app_id,"admin")
    return 20


@c.task(name="loghub.modules.applications.get_apps")
def get_apps(credential_id):
    if not credential_id:
        return 43

    user = db["users"].find_one({
                "credential_id":credential_id
                })
    
    if not user:
        return 44

    user_id = user["_id"]
    app_ids = get_user_apps(user_id)

    if not app_ids:
        return 45 

    app_list = []
    for app_id in app_ids:
        application = coll.find_one({
            "_id":app_id
            })
        if not application:
            return 46
        application["_id"] = str(application["_id"])
        app_list.append(application)
        
    return app_list

@c.task(name="loghub.modules.applications.delete_apps")
def delete_apps(APP_TOKEN,credential_id):
    user = db["users"].find_one({
                "credential_id":credential_id
                })
    if not user:
        return 20

    user_id = user["_id"]
    app = coll.find_one({
           "APP_TOKEN":APP_TOKEN,
            })
    if not app:
        return 47
    app_id = app["_id"]
    try:
        if is_admin(app_id, user_id):
            coll.remove(app)
            return 20
    except:
        return 48

@c.task(name="loghub.modules.applications.reset_app_token")
def reset_app_token(old_app_token,credential_id):
    if not old_app_token and  not credential_id:
        return 49
    if not old_app_token:
        return 47
    if not credential_id:
        return 43
    record = coll.find_one({"APP_TOKEN":old_app_token})
    if not record:
        return 45

    variable = str(math.floor(time.time())    )
    NEW_APP_TOKEN = hashlib.md5((record["name"] + credential_id + variable).encode('utf8')).hexdigest()
    record["APP_TOKEN"] = NEW_APP_TOKEN
    try:
        coll.save(record)
        return 20

    except:
        return 50