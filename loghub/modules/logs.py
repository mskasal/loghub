from loghub.storage import db
from loghub.modules.privileges import get_user_apps
from loghub.flask_celery import logs as c


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
        return 20
    except:
        return 52

@c.task(name="loghub.modules.logs.query_log")
def query_log(credential_id, APP_TOKENS=None, query_limit=100,
            sorted_by= -1, keyword=None,
            level=None, newer_than=None, older_than=None
            ):
    if not APP_TOKENS:
        user = db["users"].find_one({
                "credential_id":credential_id
                })
        user_id = user["_id"]
        APP_TOKENS = get_user_apps(user_id)

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
    
    for APP_TOKEN in APP_TOKENS:
        query["APP_TOKEN"] = APP_TOKEN
        log_entries = coll.find(
                        query
                        ).sort("date",sorted_by).limit(query_limit)
        if not log_entries:
            return 54

        for entry in log_entries:
            result.append(entry)

    return result