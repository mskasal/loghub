from bson.objectid import ObjectId
from loghub.storage import db
from loghub.modules.privileges import get_user_apps
from flask_celery import loghub_worker as c
import datetime
from math import ceil

collection_name = "logs"
coll = db[collection_name]


@c.task(name="loghub.modules.logs.logging")
def logging(APP_TOKEN, entry):
    if not APP_TOKEN:
        return 47

    if not entry:
        return 51

    app = db.apps.find_one({"APP_TOKEN": APP_TOKEN})
    if not app:
        return 57

    entry["appid"] = str(app["_id"])
    #entry["date"] = str(datetime.datetime.utcnow())
    if "date" not in entry:
        return 56

    new_entry = {
        "level": entry["level"],
        "appid": entry["appid"],
        "date": entry["date"],
        "metadata": entry["metadata"],
        "message": entry["message"]
    }
    try:
        coll.insert(new_entry.copy())
        del new_entry["appid"]
        return new_entry
    except:
        return 52

@c.task(name="loghub.modules.logs.query_log")
def query_log(credential_id, logfilter):
    if "page" not in logfilter:
        logfilter["page"] = 1
    else:
        try:
            logfilter["page"] = int(logfilter["page"][0])
        except:
            logfilter["page"] = 1

    if "limit" not in logfilter:
        logfilter["limit"] = 100
    else:
        try:
            logfilter["limit"] = int(logfilter["limit"][0])
        except:
            logfilter["limit"] = 100
        if logfilter["limit"] > 500:
            logfilter["limit"] = 500

    if "APP_TOKENS" not in logfilter:
        user = db["users"].find_one({"credential_id": credential_id})
        app_ids = {"$in": [str(each) for each in get_user_apps(user["_id"])]}

    else:
        logfilter["APP_TOKENS"] = logfilter["APP_TOKENS"][0].split(",")
        req_apps = list(db.apps.find({
            "APP_TOKEN": {"$in": logfilter["APP_TOKENS"]}
            }))
        app_ids = {"$in": [str(app["_id"]) for app in req_apps]}

    query = {}
    query["appid"] = app_ids
    if "keyword" in logfilter:
        query["message"] = {"$regex": "|".join(logfilter["keyword"])}

    if "level" in logfilter:
        query["level"] = {"$in": logfilter["level"][0].split(",")}

    if "newer_than" in logfilter:
        query["date"] = {"$gt": logfilter["newer_than"][0]}

    if "older_than" in logfilter:
        query["date"] = {"$lt": logfilter["older_than"][0]}

    log_entries = sorted(list(coll.find(query, {"_id": 0})), key=lambda x: x["date"])
    page_count = ceil(len(log_entries) / logfilter["limit"])
    log_entries = log_entries[(logfilter["page"]-1)*logfilter["limit"] : logfilter["page"]*logfilter["limit"]]
    app_ids = list({ObjectId(each["appid"]) for each in log_entries})
    apps = db.apps.find({"_id": {"$in": app_ids}}, {"_id": 1, "APP_TOKEN": 1})
    app_dictionary = dict([(str(app["_id"]), str(app["APP_TOKEN"])) for app in apps])
    apps = list(apps)
    for i in range(len(log_entries)):
        log_entries[i]["APP_TOKEN"] = app_dictionary[str(log_entries[i]["appid"])]
        del log_entries[i]["appid"]
    return {"entries": log_entries, "total_page_count": page_count}