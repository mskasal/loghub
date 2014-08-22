from bson.objectid import ObjectId
from loghub.storage import db
from loghub.modules.privileges import get_user_apps
from flask_celery import loghub_worker as c



collection_name = "logs"
coll = db[collection_name]


@c.task(name="loghub.modules.logs.logging")
def logging(APP_TOKEN, entry):
    if not APP_TOKEN:
        return 47

    if not entry:
        return 51

    app = db.apps.find_one({"APP_TOKEN": APP_TOKEN})
    
    entry["appid"] = str(app["_id"])
    try:
        coll.insert(entry)
        return entry
    except:
        return 52

@c.task(name="loghub.modules.logs.query_log")
def query_log(credential_id, logfilter):
    if "limit" not in logfilter:
        logfilter["limit"] = 100
    else:
        logfilter["limit"] = int(logfilter["limit"])

    if "APP_TOKENS" not in logfilter:
        user = db["users"].find_one({"credential_id": credential_id})
        app_ids = {"$in": get_user_apps(user["_id"])}
        app_ids["$in"] = [str(each) for each in app_ids["$in"]]

    else:
        req_apps = list(db.apps.find({
            "APP_TOKEN": {"$in": logfilter["APP_TOKENS"]}
            }))
        app_ids = {"$in": [str(app["_id"]) for app in req_apps]}

    query = {}
    query["appid"] = app_ids

    if "keyword" in logfilter:
        query["log"] = {"$regex": logfilter["keyword"]}

    if "level" in logfilter:
        query["level"] = {"$in": logfilter["level"].split(",")}

    if "newer_than" in logfilter:
        query["date"] = {"$gt": logfilter["newer_than"]}

    if "older_than" in logfilter:
        query["date"] = {"$lt": logfilter["older_than"]}

    log_entries = sorted(list(coll.find(query)), key=lambda x: x["date"])[:logfilter["limit"]]

    if not log_entries:
        return 54

    return log_entries