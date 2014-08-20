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
    
    entry["APP_TOKEN"] = APP_TOKEN
    
    try:
        coll.insert(entry)
        return entry
    except:
        return 52

@c.task(name="loghub.modules.logs.query_log")
def query_log(credential_id, APP_TOKENS=None, query_limit=100,
            sorted_by= -1, keyword=None,
            level=None, newer_than=None, older_than=None
            ):
    if not query_limit:
        query_limit = 100

    if not APP_TOKENS:
        user = db["users"].find_one({
                "credential_id":credential_id
                })
        user_id = user["_id"]
        app_ids = get_user_apps(user_id)

    query = {}


    if keyword is not None:
        query["log"] = {}
        query["log"]["$regex"] = keyword

    if level is not None:
        query["level"] = level

    if newer_than is not None:
        query["date"] = {}
        query["date"]["$gt"] = newer_than

    if older_than is not None:
        query["date"] = {}
        query["date"]["$lte"] = older_than

    result = []
    print(app_ids)

    for app_id in app_ids:
        app = db.apps.find_one({"_id":app_id})
        print(app)
        APP_TOKEN = app["APP_TOKEN"]

        if not APP_TOKEN:
            continue

        query["APP_TOKEN"] = APP_TOKEN

        log_entries = list(coll.find(
                        query
                        ).sort("date",sorted_by).limit(query_limit))
               
        if not log_entries:
            continue

        for entry in log_entries:
            result.append(entry)
    if not result:
        return 54

    return result